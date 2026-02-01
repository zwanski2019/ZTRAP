import streamlit as st
import os
import subprocess
import sys
import importlib.util
import re

TOOLS_DIR = "dynamic_tools"

# Ensure the directory exists
if not os.path.exists(TOOLS_DIR):
    os.makedirs(TOOLS_DIR)


def validate_and_install_deps(file_content: str):
    """Scans the code for 'import' statements and installs missing libs."""
    # Find all 'import x' or 'from x import y'
    # allow leading whitespace before import statements
    imports = re.findall(r"^\s*(?:import|from)\s+([\w\d_]+)", file_content, re.MULTILINE)

    standard_libs = sys.builtin_module_names
    for lib in set(imports):
        # Skip builtins and streamlit itself
        if lib in standard_libs or lib == "streamlit":
            continue
        try:
            st.info(f"📦 Resolving dependency: {lib}...")
            subprocess.run([sys.executable, "-m", "pip", "install", lib], check=True)
        except Exception as e:
            st.error(f"❌ Failed to install {lib}: {e}")


def tool_forge_panel():
    st.header("🛠️ Zwanski Tool-Forge (Admin)")
    st.write("Upload a Python script to instantly integrate it as a ZTRAP tool.")

    uploaded_file = st.file_uploader("Upload Python Tool", type=["py"])

    if uploaded_file is not None:
        file_name = uploaded_file.name
        file_path = os.path.join(TOOLS_DIR, file_name)
        file_content = uploaded_file.getvalue().decode("utf-8")

        if st.button(f"DEPLOY {file_name.upper()}"):
            with st.spinner("Validating & Syncing..."):
                # 1. Dependency Resolution
                validate_and_install_deps(file_content)

                # 2. Save the file to dynamic_tools/
                with open(file_path, "w") as f:
                    f.write(file_content)

                st.success(f"🚀 {file_name} has been hot-deployed to the Master Repository.")

                # Regenerate sitemap to include new tool
                try:
                    from seo import regenerate_sitemap
                    regenerate_sitemap(get_dynamic_tools())
                    st.info("Sitemap updated with deployed tool.")
                except Exception as e:
                    st.warning(f"Failed to update sitemap automatically: {e}")

                st.rerun()

    st.markdown("---")
    st.subheader("Static File Manager (SEO & Verification)")
    st.write("Upload static files (e.g., verification HTML, sitemap.xml, robots.txt). These will be served from `/app/static/` when deployed.")

    static_upload = st.file_uploader("Upload Static File", key="static_upload")
    if static_upload is not None:
        sname = static_upload.name
        scontent = static_upload.getvalue().decode("utf-8")
        publish_to_static = st.checkbox("Publish to site static folder (public)", value=False)

        if publish_to_static:
            st.warning("You are about to publish a file publicly under /app/static/.")
            confirm = st.checkbox("I understand the security implications and confirm publish.")
            if st.button(f"PUBLISH {sname}"):
                if not confirm:
                    st.error("Publish not confirmed. Check the confirmation box to proceed.")
                else:
                    # Save to static/
                    try:
                        os.makedirs('static', exist_ok=True)
                        with open(os.path.join('static', sname), 'w', encoding='utf-8') as sf:
                            sf.write(scontent)
                        st.success(f"Static file {sname} published to /app/static/{sname}")
                    except Exception as e:
                        st.error(f"Failed to publish static file: {e}")



def get_dynamic_tools():
    """Returns a list of all deployed tools in the forge."""
    try:
        return [f[:-3] for f in os.listdir(TOOLS_DIR) if f.endswith(".py")]
    except FileNotFoundError:
        return []


def run_dynamic_tool(tool_name: str):
    """Dynamically imports and executes the 'run()' or 'main()' function of a tool."""
    file_path = os.path.join(TOOLS_DIR, f"{tool_name}.py")
    if not os.path.exists(file_path):
        st.error(f"Tool not found: {tool_name}")
        return

    spec = importlib.util.spec_from_file_location(tool_name, file_path)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        st.error(f"Failed to load tool '{tool_name}': {e}")
        return

    # Requirement: Your uploaded tools MUST have a run() or main() function
    if hasattr(module, "run") and callable(module.run):
        try:
            module.run()
        except Exception as e:
            st.error(f"Tool execution failed: {e}")
    elif hasattr(module, "main") and callable(module.main):
        try:
            module.main()
        except Exception as e:
            st.error(f"Tool execution failed: {e}")
    else:
        st.error("❌ Tool format error: No run() or main() function found in script.")
