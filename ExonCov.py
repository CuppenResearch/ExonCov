#!venv/bin/python
"""ExonCov CLI."""
from flask_script import Manager

from ExonCov import app, cli

db_manager = Manager(usage='Database commands.')
manager = Manager(app)

manager.add_command("db", db_manager)
manager.add_command('import_bam', cli.ImportBam())
manager.add_command('search_sample', cli.SearchSample())
manager.add_command('remove_sample', cli.RemoveSample())
manager.add_command('check_samples', cli.CheckSamples())

db_manager.add_command('stats', cli.PrintStats())
db_manager.add_command('panel_genes', cli.PrintPanelGenesTable())
#db_manager.add_command('load_design', cli.LoadDesign())

if __name__ == "__main__":
    manager.run()