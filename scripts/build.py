import glob
import os
import re
import shutil

from jinja2 import Environment, FileSystemLoader


class Build(object):
    def __init__(self, *args, **kwargs):
        self.parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.build_dir = os.path.join(self.parent_dir, 'build')
        self.data_dir = os.path.join(self.parent_dir, 'data')
        self.src_dir = os.path.join(self.parent_dir, 'src')
        self.manifest_template = Environment(loader=FileSystemLoader(self.parent_dir)).get_template('manifest.json.j2')

    def build(self):
        breadcrumbs_file_paths = glob.glob(os.path.join(self.data_dir, '*-breadcrumbs.json'))
        countries = set([re.search(r'(.{2})-breadcrumbs.json', path).groups()[0] for path in breadcrumbs_file_paths])
        for country in countries:
            self.build_country(country)

    def build_country(self, country):
        # remove and recreate country build dir from src dir
        country_dir = os.path.join(self.build_dir, country)
        shutil.rmtree(country_dir, ignore_errors=True)
        shutil.copytree(self.src_dir, country_dir)

        # find and copy breadcrumbs
        country_breadcrumbs_file_paths = glob.glob(os.path.join(self.data_dir, '*{}-breadcrumbs.json'.format(country)))
        for breadcrumbs_path in country_breadcrumbs_file_paths:
            shutil.copy(breadcrumbs_path, country_dir)

        # find sites
        pattern = r'www\.(?P<domain>.*)-(?P<region>.{2}-.{2})-breadcrumbs.json'
        sites = [re.search(pattern, path).groupdict() for path in country_breadcrumbs_file_paths]

        # render and write manifest
        manifest = self.manifest_template.render(country_code=country, sites=sites)
        with open(os.path.join(country_dir, 'manifest.json'), 'w') as f:
            f.write(manifest)

        # make archive
        shutil.make_archive(
            base_name=os.path.join(self.build_dir, 'extension-{country}'.format(country=country)),
            format='zip',
            root_dir=country_dir,
        )


if __name__ == '__main__':
    build = Build()
    build.build()
