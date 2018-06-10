import glob
import os
import re
import shutil

from jinja2 import Environment, FileSystemLoader


class Build(object):
    def __init__(self, *args, **kwargs):
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.src_dir_path = os.path.join(parent_dir, 'src')
        self.build_dir_path = os.path.join(parent_dir, 'build')
        self.manifest_template = Environment(loader=FileSystemLoader(self.src_dir_path)).get_template('manifest.json.j2')

    def build(self):
        breadcrumbs_file_paths = glob.glob(os.path.join(self.src_dir_path, '*-breadcrumbs.json'))
        countries = set([re.search(r'(.{2})-breadcrumbs.json', path).groups()[0] for path in breadcrumbs_file_paths])
        for country in countries:
            self.build_country(country)

    def build_country(self, country):
        pattern = r'www\.(?P<domain>.*)-(?P<region>.{2}-.{2})-breadcrumbs.json'
        country_breadcrumbs_file_paths = glob.glob(os.path.join(self.src_dir_path, '*{}-breadcrumbs.json'.format(country)))
        sites = [re.search(pattern, path).groupdict() for path in country_breadcrumbs_file_paths]
        manifest = self.manifest_template.render(country_code=country, sites=sites)

        dir_path = os.path.join(self.build_dir_path, country)
        shutil.rmtree(dir_path)
        os.mkdir(dir_path)
        with open(os.path.join(dir_path, 'manifest.json'), 'w') as f:
            f.write(manifest)


if __name__ == '__main__':
    build = Build()
    build.build()
