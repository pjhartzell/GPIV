import click
from piv_functions import format_input, ingest_data, run_piv
from show_functions import show


@click.group()
def cli():
    pass


@click.command()
@click.argument('before', type=click.Path(exists=True, readable=True))
@click.argument('after', type=click.Path(exists=True, readable=True))
@click.argument('template_size', type=click.IntRange(3, None))
@click.argument('step_size', type=click.IntRange(1, None))
@click.option('--iternum', type=click.IntRange(1, None), default=3, help='Option to set number of correlation passes. Default value is 3.')
@click.option('--outname', type=str, help='Optional base filename to use for output files.')
@click.option('--propagate', nargs=2, type=click.Path(exists=True, readable=True), help='Option to propagate error. Requires two arguments: 1) pre-event uncertainties in GeoTIFF format, 2) post-event uncertainties in GeoTIFF format.')
def piv(before, after, template_size, step_size, iternum, outname, propagate):
    '''
    Runs PIV on a pair pre- and post-event DEMs.

    \b
    Arguments: BEFORE  Pre-event data (e.g., a DEM) in GeoTIFF format
               AFTER   Post-event data (e.g., a DEM) in GeoTIFF format
               TEMPLATE_SIZE  Size of square correlation template in pixels
               STEP_SIZE      Size of template step in pixels
    '''
    # Format user input
    user_input = format_input(before, after,
                              template_size, step_size,
                              iternum, outname, propagate)

    # Ingest user supplied before and after images
    image_data = ingest_data(user_input)

    # Launch image correlation process
    run_piv(user_input, image_data)


@click.command()
@click.argument('background_image', type=click.Path(exists=True, readable=True))
@click.option('--vec', type=click.Path(exists=True, readable=True), help="Option to overlay PIV vectors on the background image. Requires the json file of PIV vectors generated by the 'piv' command.")
@click.option('--ell', type=click.Path(exists=True, readable=True), help="Option to overlay PIV uncertainty ellipses on the background image. Requires the json file of covariance matrices generated when running the 'piv' command with the 'prop' option.")
@click.option('--vecscale', type=float, help='Option to scale the displayed PIV vectors. Requires a numeric scale factor.')
@click.option('--ellscale', type=float, help='Option to scale the displayed uncertainty ellipses. Requires a numeric scale factor.')
def pivshow(background_image, vec, ell, vecscale, ellscale):
    '''
    Optionally displays PIV displacement vectors and/or uncertainty ellipses over a background image.
    
    Arguments: BACKGROUND_IMAGE  Background image in GeoTIFF format
    '''
    show(background_image,
         vector_file=vec,
         covariance_file=ell,
         vector_scale=vecscale,
         ellipse_scale=ellscale)


cli.add_command(piv)
cli.add_command(pivshow)

if __name__ == '__main__':
    cli()
