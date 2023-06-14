import subprocess


def run_streamlit():
    # ruft die Streamlit start bedingung auf "streamlit run Gefaehrdungskatalog.py"
    subprocess.run(["streamlit", "run", "Gefaehrdungskatalog.py"])


if __name__ == '__main__':
    run_streamlit()
