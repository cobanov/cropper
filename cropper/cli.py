import click

from cropper.smartcrop import main as smartcrop


@click.command()
@click.argument("filelist", type=click.Path())
@click.option(
    "--outdir", type=click.Path(exists=True), help="Path to write cropped images"
)
@click.option("--crop", type=click.BOOL, default=False, help="Crop images")
@click.option(
    "--square", type=click.BOOL, default=True, help="Create square crop of all images"
)
def cropper(filelist, outdir, crop, square):
    """
    Smartcropper to find best crop from image

    Arguments:

        FILELIST: Path to filelist of images to be cropped
    """
    smartcrop(filelist, outdir, crop, square)


if __name__ == "__main__":
    cropper()
