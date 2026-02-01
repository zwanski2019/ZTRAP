# Tool-Forge Admin Panel

This feature allows admins to upload Python tools which are stored in `dynamic_tools/` and dynamically loaded into the app sidebar.

How it works

- Upload a .py file via the `ADMIN-FORGE` panel (or `admin_forge.tool_forge_panel()` if used programmatically).
- The script is scanned for `import` statements and `pip` is invoked to install non-builtins (excluding `streamlit`).
- The file is written to `dynamic_tools/` and the app performs a `st.rerun()` so the tool appears in the menu instantly.
- Tools must include `run()` or `main()` which will be executed when the menu item is selected.

Security notes

- Be careful installing arbitrary packages on a host — this can be a security risk. Consider running the server in an isolated environment or container.
- Uploaded scripts are executed with the server's privileges. Treat uploads as trusted or add additional verification steps before execution.
