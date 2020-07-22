import os
import click
from converter import  bin_pcd_converter


@click.command()
@click.argument('input_path', type=click.Path(exists=True), required=True)
@click.argument('output_folder', type=click.Path(exists=True), required=True)
def main(input_path, output_folder):
    """Conversion tool for the point cloud formats .bin and .pcd"""
    
    # Check input arguments
    input_isfile = os.path.isfile(input_path)
    input_isdir = os.path.isdir(input_path)
    if (not input_isfile) and (not input_isdir):
        click.echo('Input path should be an existing file or directory!', err=True)
        return()
    
    output_isdir = os.path.isdir(output_folder)
    if (not output_isdir):
        click.echo('Output path should be an existing directory!', err=True)
        return()
    
    # Log input arguments
    click.echo('Start converting')
    click.echo(f' - input path: {input_path}')
    click.echo(f' - output path: {output_folder}')

    # Convert file(s)
    if input_isfile:
        bin_pcd_converter(input_path, output_folder)
    else:
        filewalk = os.walk(input_path, topdown=False)
        for root, dirs, files in filewalk:
            for name in files:
                input_file = os.path.join(root, name)
                bin_pcd_converter(input_file, output_folder)

    click.echo('Done.')

if __name__ == '__main__':
    main()

    