import os
import shutil
import subprocess
import tempfile
from typing import Tuple

OPENCLAW_ENV_VAR = "ZTRAP_ENABLE_OPENCLAW"
SIMULATION_ENV_VAR = "ZTRAP_OPENCLAW_SIMULATE"

def install_openclaw():
    """Automated installation of OpenClaw via official curl script."""
    st.warning("⚙️ Installing OpenClaw (Moltbot) Framework...")
    try:
        # Run the official installer
        cmd = "curl -fsSL https://openclaw.ai/install.sh | bash"
        subprocess.run(cmd, shell=True, check=True)
        st.success("✅ OpenClaw Installed. Initializing Onboarding...")
        # Launch the onboarding wizard in a separate terminal for the user
        os.system("x-terminal-emulator -e 'moltbot onboard'")
    except Exception as e:
        st.error(f"❌ Installation failed: {e}")

def get_openclaw_status():
    """Check if the gateway is running."""
    try:
        # Check if the process 'moltbot' or 'openclaw' is in the process list
        output = subprocess.check_output(["ps", "aux"]).decode()
        return "openclaw" in output.lower() or "moltbot" in output.lower()
    except:
        return False


def node_installed() -> bool:
    """Return True if node/npm are available on PATH."""
    return shutil.which("node") is not None and shutil.which("npm") is not None


def openclaw_installed() -> bool:
    """Detect presence of the 'moltbot' CLI on PATH."""
    return shutil.which("moltbot") is not None


def get_status() -> dict:
    """Return a small status dict describing environment and simulation mode."""
    return {
        "node": node_installed(),
        "moltbot": openclaw_installed(),
        "simulate": os.getenv(SIMULATION_ENV_VAR) == "1",
        "enabled": os.getenv(OPENCLAW_ENV_VAR) == "1",
    }


def install_instructions() -> str:
    """Return safe manual installation instructions (review-first).

    This explicitly avoids executing remote installers from the web UI.
    """
    return (
        "Manual installation instructions for OpenClaw (Moltbot):\n\n"
        "1) Inspect the official installer: https://openclaw.ai/install.sh\n"
        "2) Download the installer locally for review:\n"
        "   curl -fsSL https://openclaw.ai/install.sh -o /tmp/openclaw_install.sh\n"
        "   less /tmp/openclaw_install.sh  # review before executing\n"
        "3) Execute only after review and inside a disposable VM or unprivileged user:\n"
        "   bash /tmp/openclaw_install.sh\n\n"
        "Important: Never run an installer without reviewing it first. Prefer a disposable VM or container."
    )


def prepare_install_dry_run(download_to: str = None) -> tuple:
    """Download the installer for local review without executing it.

    If SIMULATION_ENV_VAR==1, create a fake installer file instead (no network).
    """
    if os.getenv(SIMULATION_ENV_VAR) == "1":
        fd, path = tempfile.mkstemp(prefix="openclaw_install_")
        with os.fdopen(fd, "w") as f:
            f.write("# SIMULATED OpenClaw installer for local review\n# No network actions performed in simulation mode.\n")
        return True, path

    if download_to is None:
        download_to = os.path.join(tempfile.gettempdir(), "openclaw_install.sh")

    # Download the installer only (do not execute it). Caller must review before running.
    cmd = ["curl", "-fsSL", "https://openclaw.ai/install.sh", "-o", download_to]
    subprocess.run(cmd, check=True)
    return True, download_to


def start_gateway_command() -> str:
    """Return the safe command the operator can run locally to start the gateway."""
    return "nohup moltbot gateway > agent.log 2>&1 &"