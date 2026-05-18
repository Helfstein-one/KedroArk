import typer
from rich.console import Console
from cookiecutter.main import cookiecutter
import os

app = typer.Typer(help="KedroArk CLI - Scaffold Kedro projects for AWS")
console = Console()

KEDRO_ARK_BANNER = r"""
[bold magenta]
  _  __       _             _         _
 | |/ /      | |           / \   _ __| | __
 | ' / ___ __| |_ __ ___  / _ \ | '__| |/ /
 | . \/ _ / _` | '__/ _ \/ ___ \| |  |   <
 |_|\_\___\__,_|_|  \___/_/   \_\_|  |_|\_\
[/bold magenta]
[bold cyan]Scaffold Enterprise Kedro Pipelines for AWS[/bold cyan]
"""

def show_banner():
    console.print(KEDRO_ARK_BANNER)

@app.command()
def init(
    project_name: str = typer.Argument(..., help="Name of the new Kedro project"),
    compute: str = typer.Option(
        "AWS Glue", "--compute", "-c",
        help="Target compute engine: 'AWS Glue', 'AWS EMR', or 'AWS EMR Serverless'"
    ),
    example: str = typer.Option(
        "no", "--example", "-e",
        help="Include an example pipeline? Pass 'finance' for the financial Iceberg example."
    ),
    local_infra: bool = typer.Option(
        False, "--local-infra", "-l",
        help="Include a docker-compose setup with MinIO to test S3 interactions locally."
    )
):
    """
    Initialize a new Kedro project with AWS infrastructure support.
    """
    show_banner()
    console.print(f"[bold green]Initializing KedroArk project: {project_name}[/bold green]")
    console.print(f"Target Compute: [bold cyan]{compute}[/bold cyan]")

    include_finance = "yes" if example.lower() == "finance" else "no"
    include_local_infra = "yes" if local_infra else "no"

    # Define the template directory path
    template_dir = os.path.join(os.path.dirname(__file__), "templates", "project")

    extra_context = {
        "project_name": project_name,
        "compute_target": compute,
        "include_finance_example": include_finance,
        "include_local_infra": include_local_infra
    }

    try:
        cookiecutter(
            template_dir,
            no_input=True,
            extra_context=extra_context,
            output_dir="."
        )
        console.print("[bold green]Project created successfully![/bold green]")

        # Determine the generated project directory
        project_slug = project_name.lower().replace(' ', '_').replace('-', '_')

        # Run some post-generate cleanup if needed based on compute target
        _post_generate(project_slug, compute, include_finance)

    except Exception as e:
        console.print(f"[bold red]Failed to create project: {e}[/bold red]")

def _post_generate(project_slug: str, compute: str, include_finance: str):
    """Handle dynamic removal or adjustments after generation."""

    # Optional: cleanup terraform files based on compute choice if cookiecutter jinja wasn't enough
    pass

@app.command()
def test_local(
    env: str = typer.Option("local_infra", "--env", help="Kedro environment to use for local testing.")
):
    """
    Start local infrastructure (MinIO) using docker-compose and run the Kedro pipeline locally.
    """
    show_banner()
    console.print("[bold green]Starting local infrastructure (MinIO)...[/bold green]")
    import subprocess

    if not os.path.exists("docker-compose.yml"):
        console.print("[bold red]Error: docker-compose.yml not found. Did you initialize with --local-infra?[/bold red]")
        raise typer.Exit(1)

    try:
        subprocess.run(["docker-compose", "up", "-d"], check=True)
        # Determine which compute target service exists in docker-compose
        with open("docker-compose.yml", "r") as f:
            compose_content = f.read()

        service_to_run = None
        if "glue-dev:" in compose_content:
            service_to_run = "glue-dev"
        elif "emr-submit:" in compose_content:
            service_to_run = "emr-submit"
        elif "emr-serverless-emulator:" in compose_content:
            service_to_run = "emr-serverless-emulator"

        if service_to_run:
            console.print(f"[bold cyan]Detected target compute. Running {service_to_run}...[/bold cyan]")
            subprocess.run(["docker-compose", "up", "--build", "--abort-on-container-exit", service_to_run], check=True)
        else:
            # Fallback to local execution if no dedicated service is found
            subprocess.run(["kedro", "run", "--env", env], check=True)

    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Pipeline or infrastructure failed: {e}[/bold red]")
    finally:
        console.print("[bold yellow]Tearing down local infrastructure...[/bold yellow]")
        subprocess.run(["docker-compose", "down"])

if __name__ == "__main__":
    app()
