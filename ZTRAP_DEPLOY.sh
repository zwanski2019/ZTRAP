#!/bin/bash
# ZTRAP Installer for Kali
go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
sudo cp ~/go/bin/* /usr/local/bin/
echo "Kali tools ready. Now run 'streamlit run app.py'"
