"""A scripted stand-in for the model (SIMULATED: no model runs). An OpenAI-compatible /v1/chat/completions server
that, turn by turn, makes the calls the prompt asks for, so the real harness, compiler, skill toolset and sandbox run
end to end on CPU:
  1. run_skill_script(skill_name=edit-fallback, file_path=scripts/install.py)   (no other argument)
  2. run_command: python3 /tmp/h/find.py <name>
  3. run_command: python3 /tmp/h/edit.py <top file> --dry-run   with a SEARCH line copied from find.py's output,
     damaged the QAT way (a final "s" dropped) so the close-match path runs
  4. run_command: python3 /tmp/h/edit.py <same> with the exact line (writes), then git diff --stat
  5. submit_patch
Every request and the tool results it carries are logged to harness_check_model.log.

It answers every request itself, so no GPU is used and no model is judged: it checks the plumbing (that the
compiler loads the skill, run_skill_script runs install.py in the sandbox, and the helpers are where run_command
looks), not the agent. Used for docs/fallback-scripts-study.md, "End to end in the harness".

usage: harness_check_model.py PORT NAME     then, in another shell:
  OPENAI_BASE_URL=http://127.0.0.1:PORT/v1 OPENAI_API_KEY=x swegemma eval --tasks <tasks.jsonl> \
      --snapshots-dir <snapshots> --submission-dir <copy of the submission files> --results-dir <out> \
      --sandbox subprocess --max-tool-calls 6 --max-time-minutes 5
"""
import json
import re
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT, NAME = int(sys.argv[1]), sys.argv[2]
LOG = open("harness_check_model.log", "a")


def tool_call(name, args, k):
    return {"id": f"call_{k}", "type": "function", "function": {"name": name, "arguments": json.dumps(args)}}


def plan(messages):
    tool_msgs = [m for m in messages if m.get("role") == "tool"]
    k = len(tool_msgs)
    last = tool_msgs[-1]["content"] if tool_msgs else ""
    if isinstance(last, list):
        last = " ".join(x.get("text", "") for x in last if isinstance(x, dict))
    if k == 0:
        return tool_call("run_skill_script", {"skill_name": "edit-fallback", "file_path": "scripts/install.py"}, k)
    if k == 1:
        return tool_call("run_command", {"command": f"python3 /tmp/h/find.py {NAME}"}, k)
    if k in (2, 3):
        find_out = tool_msgs[1]["content"]
        if isinstance(find_out, list):
            find_out = " ".join(x.get("text", "") for x in find_out if isinstance(x, dict))
        text = json.loads(find_out).get("stdout", find_out) if find_out.strip().startswith("{") else find_out
        m = re.search(r"^(\S+\.py)\s+\(names", text, re.M)
        line = re.search(r"^\s+\d+: (.+)$", text, re.M)
        if not (m and line):
            return tool_call("submit_patch", {}, k)
        path, src = m.group(1), line.group(1)
        search = re.sub(r"([a-z])s\b", r"\1", src, count=1) if k == 2 else src
        replace = src + "  # fallback check"
        dry = " --dry-run" if k == 2 else ""
        cmd = (f"cd /workspace && python3 /tmp/h/edit.py {path}{dry} <<'EOF'\n<<<<<<< SEARCH\n{search}\n=======\n"
               f"{replace}\n>>>>>>> REPLACE\nEOF\ngit diff --stat")
        return tool_call("run_command", {"command": cmd}, k)
    return tool_call("submit_patch", {}, k)


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
        msgs = body.get("messages", [])
        call = plan(msgs)
        LOG.write(json.dumps({"model": body.get("model"), "n_messages": len(msgs),
                              "tools": [t["function"]["name"] for t in body.get("tools", [])],
                              "last_tool_result": next((m.get("content") for m in reversed(msgs)
                                                        if m.get("role") == "tool"), None),
                              "reply": call}) + "\n")
        LOG.flush()
        resp = {"id": "fake", "object": "chat.completion", "created": 0, "model": body.get("model"),
                "choices": [{"index": 0, "finish_reason": "tool_calls",
                             "message": {"role": "assistant", "content": None, "tool_calls": [call]}}],
                "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2}}
        data = json.dumps(resp).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        data = json.dumps({"data": [{"id": "gemma-4-e4b-it-qat-w4a16-ct"}, {"id": "copyfix"}]}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *a):
        pass


HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
