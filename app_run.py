import os
import sys
import streamlit.web.cli as stcli

def resolve_path(path):
    # Αυτή η συνάρτηση βρίσκει τον προσωρινό φάκελο _MEIPASS που φτιάχνει το --onefile
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, path)
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), path)

if __name__ == "__main__":
    script_path = resolve_path("interface.py")
    
    # Περνάμε τις εντολές στο Streamlit
    sys.argv = ["streamlit", "run", script_path, "--global.developmentMode=false"]
    sys.exit(stcli.main())