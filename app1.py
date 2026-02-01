elif choice == "SYSTEM-ACCESS":
    st.header("⚡ Persistent Task Manager")
    task_name = st.text_input("Job Label", "PayPal-Sub-Takeover-Scan")
    cmd = st.text_area("Command to Background", "subfinder -d paypal.com | nuclei -t takeovers/")
    
    if st.button("DETACH & EXECUTE"):
        # Uses 'nohup' to keep the process alive after you close the browser
        subprocess.Popen(f"nohup {cmd} > {task_name}.log 2>&1 &", shell=True)
        st.success(f"Job '{task_name}' is now running in the shadow. Check Discord for results.")
