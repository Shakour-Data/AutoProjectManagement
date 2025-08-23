import subprocess

# List of recommended VS Code extensions to install
extensions = [
    "blackboxai.blackbox",  # BLACKBOX AI
    "github.vscode-pull-request-github",  # GitHub Pull Requests and Issues
    "ms-python.python",  # Python
    "yzhang.markdown-all-in-one",  # Markdown All in One
    "alefragnani.project-manager",  # Project Manager
    "mhutchie.git-graph",  # Git Graph
    "vstirbu.vscode-mermaid-preview",  # Mermaid diagram preview
    "hediet.vscode-drawio",  # Draw.io integration
    "bierner.markdown-mermaid"  # Mermaid diagrams in markdown
]

def install_extensions():
    for ext in extensions:
        print(f"Installing VS Code extension: {ext}")
        subprocess.run(["code", "--install-extension", ext], check=True)
    print("All extensions installed.")

if __name__ == "__main__":
    install_extensions()
