#!/usr/local/bin/python2.7
from bs4 import BeautifulSoup
import requests
import re
import versionstatus

class WPScraper():
    WP_DOWNLOAD = 'https://wordpress.org/download'
    WP_VERSIONS = 'https://codex.wordpress.org/WordPress_Versions'
    README_PATH = "/readme.html"
    DANGER = versionstatus.get_colour(0)
    WARN = versionstatus.get_colour(1)
    GOOD = versionstatus.get_colour(2)
    END = versionstatus.get_colour("END")

    def get_current_version(self):
        # get the WordPress download page and search for version number
        r = requests.get(self.WP_DOWNLOAD)
        match = re.search(
            r'Download&nbsp;WordPress&nbsp;([0-9]+\.[0-9]+\.[0-9]+)',
            str(r.text)
        )
        if match:
            # if it is found, return the version number
            return match.group(1)
        else:
            raise Exception('Cannot read current stable WP version')

    def get_version_date(self, version_num):
        # Get the WordPress table of versions
        r = requests.get(self.WP_VERSIONS)
        soup = BeautifulSoup(r.text, "lxml")
        tables = soup.findChildren('table')
        rows = tables[0].findChildren(['tr'])

        for row in rows:
            # search the rows for a matchin version number
            cells = row.findChildren(['td', 'th'])
            cell_version = cells[0].contents[1]
            match = re.search(version_num,cell_version.string)

            if match:
                # if there is a match, break out
                version_date = cells[1].string
                break

        if version_date:
            return version_date
        else:
            return False

    def get_domain_title(self, domain):
        try:
            r = requests.get("http://" + domain)
            soup = BeautifulSoup(r.text, "lxml")
            title = soup.title.string
            if title:
                return title
            else:
                return False
        except requests.exceptions.HTTPError as e:
            print(
                self.WARN +
                "[!]WARNING: %s has thrown an exception %s %s"
                % (domain, e, self.END)
            )

    def get_domain_version(self, domain):
        try:
            r = requests.get("http://" + domain + self.README_PATH)
            match = re.search(
                r'Version ([0-9]+\.[0-9]+\.[0-9]+)',
                str(r.text)
            )
            if match:
                version = match.group(1)
            else:
                print(
                    self.WARN +
                    "[!]WARNING: Cannont read WordPress version for %s %s"
                    % (domain, self.END)
                )
                return False
        except requests.exceptions.HTTPError:
            print(
                self.WARN +
                "[!]WARNING: Cannont read WordPress version for %s %s"
                % (domain, self.END)
            )

        return version

    def get_domain_info(self, domain):
        domain_info = {}
        domain_info["version"] = self.get_domain_version(domain)
        domain_info["title"] = self.get_domain_title(domain)

        return domain_info
