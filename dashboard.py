diff --git a//dev/null b/dashboard.py
index 0000000000000000000000000000000000000000..51f0108104282feb15f4c6f603c5bb95d1e0a08f 100644
--- a//dev/null
+++ b/dashboard.py
@@ -0,0 +1,62 @@
+import json
+import streamlit as st
+from pathlib import Path
+
+st.set_page_config(page_title="Ghost Protocol Reflection Engine", layout="wide")
+
+# Apply basic dark theme styling
+st.markdown(
+    """
+    <style>
+    body { background-color: #111; color: #eee; }
+    .st-bb { background-color: #222; }
+    .st-b0 { background-color: #222; }
+    </style>
+    """,
+    unsafe_allow_html=True,
+)
+
+# Load mock data
+data_path = Path("data/mock_outputs.json")
+if data_path.exists():
+    with data_path.open() as f:
+        data = json.load(f)
+else:
+    st.error("Mock data not found.")
+    st.stop()
+
+scores = data.get("scores", {})
+red_flags = data.get("red_flags", [])
+logs = data.get("simulation_log", [])
+
+st.title("Ghost Protocol Reflection Engine")
+
+# Scoring Panel
+with st.expander("Scoring Panel", expanded=True):
+    cols = st.columns(3)
+    score_keys = [
+        ("Foresight Health", scores.get("foresight_health", {})),
+        ("Culture Resilience", scores.get("culture_resilience", {})),
+        ("Narrative Alignment", scores.get("narrative_alignment", {})),
+    ]
+    for col, (label, item) in zip(cols, score_keys):
+        with col:
+            st.metric(label, item.get("score", 0))
+            st.caption(item.get("text", ""))
+
+# Red Flag Summary Section
+with st.expander("Red Flag Summary", expanded=True):
+    severity_groups = {"High": [], "Medium": [], "Low": []}
+    for flag in red_flags:
+        severity_groups.setdefault(flag.get("severity", "Low"), []).append(flag.get("tag", ""))
+    for severity, tags in severity_groups.items():
+        st.subheader(severity)
+        for t in tags:
+            st.write(t)
+
+# Simulation Log
+with st.expander("Simulation Log", expanded=True):
+    for entry in logs:
+        st.write(f"[{entry['timestamp']}] {entry['prompt']} -> {entry['response']}")
+
+st.write("\n*Internal use only*")
