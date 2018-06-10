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
        pattern = r'www\.(?P<domain>.*)-(?P<region>.{2}-.{2})-breadcrumbs.json'
        country_breadcrumbs_file_paths = glob.glob(os.path.join(self.data_dir, '*{}-breadcrumbs.json'.format(country)))
        sites = [re.search(pattern, path).groupdict() for path in country_breadcrumbs_file_paths]
        manifest = self.manifest_template.render(country_code=country, sites=sites)

        dir_path = os.path.join(self.build_dir, country)
        try:
            shutil.rmtree(dir_path)
        except FileNotFoundError:
            pass
        os.mkdir(dir_path)
        with open(os.path.join(dir_path, 'manifest.json'), 'w') as f:
            f.write(manifest)


if __name__ == '__main__':
    build = Build()
    build.build()
