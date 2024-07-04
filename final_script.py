import os
import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from conceptnet.conceptnet_module import query_conceptnet
from translator import Translator

GPT = "GPT"
LLAMA = "LLAMA"

app = typer.Typer()
console = Console()


@app.command()
def main(
        final_results_path: str = typer.Option(default="./",
                                               prompt="Please, enter the folder where to save the final results"),
        folder_path: str = typer.Option("./",
                                        prompt="Please, enter the path of the folder in which your files about the "
                                               "crime case are"),
        llm_translator: str = typer.Option(GPT,
                                           prompt="Please, enter the large language model that you prefer to use "
                                                  "to translate the knowledge. (GPT or LLAMA)")
):
    keywords = ['crime_scene', '_report']

    if not os.path.isdir(folder_path):
        console.print(f"[bold red]Error: The folder path '{folder_path}' is not valid.[/bold red]")
        raise typer.Exit()
    if not os.path.isdir(final_results_path):
        console.print(f"[bold red]Error: The final results path '{final_results_path}' is not valid.[/bold red]")
        raise typer.Exit()

    filtered_files = []
    for file_name in os.listdir(folder_path):
        file_path = folder_path + "/" + file_name
        #file_path = os.path.join(folder_path, file_name)
        console.print(f"Checking file: {file_path}")
        if any(keyword in file_name for keyword in keywords):
            console.print(f"[bold green]Matched keyword in file: {file_path}[/bold green]")
            filtered_files.append(file_name)
        else:
            console.print(f"[bold yellow]No keyword match in file: {file_path}[/bold yellow]")

    if not filtered_files:
        console.print(
            f"[bold red]Error: No files containing the specified keywords were found in '{folder_path}'.[/bold red]")
        raise typer.Exit()

    if llm_translator != GPT and llm_translator != LLAMA:
        console.print(
            f"[bold red]Error: Inserted wrong large language model name.[/bold red]")
        raise typer.Exit()

    with Progress(SpinnerColumn(),
                  TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        translation_task = progress.add_task("[bold green]Starting translation...[/bold green]", total=None)
        translator = Translator(llm_translator)
        translator.make_translation(folder_path, filtered_files)
        progress.remove_task(translation_task)

        scanner_task = progress.add_task("[bold green]Starting scanner...[/bold green]", total=None)
        translator.write_translation_outputs(final_results_path)
        progress.remove_task(scanner_task)

    entities_file_path = typer.prompt("Please, enter the path of the file in which the words you want "
                                      "to know commonsense knowledge about are located",
                                      default="./")
    if not os.path.exists(entities_file_path):
        console.print(
            f"[bold red]Error: The path does not exist. Please enter a valid path.[/bold red]")
        raise typer.Exit()

    with Progress(SpinnerColumn(),
                  TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        conceptnet_task = progress.add_task("[bold green]Querying ConceptNet...[/bold green]", total=None)
        query_conceptnet(entities_file_path, final_results_path)
        progress.remove_task(conceptnet_task)

    console.print("[bold green]All the ASP facts are now written in the specified folder.[/bold green]")


if __name__ == "__main__":
    app()
