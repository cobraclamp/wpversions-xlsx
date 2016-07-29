#!/usr/local/bin/python2.7
from wpvscraper import WPScraper
import versionstatus
import helpers
import concurrent.futures
from datetime import datetime
from collections import OrderedDict
from operator import itemgetter


class Scanner():
    MAX_WORKERS = 5
    DANGER = versionstatus.get_colour(0)
    WARN = versionstatus.get_colour(1)
    GOOD = versionstatus.get_colour(2)
    END = versionstatus.get_colour("END")

    def __init__(self, domains_file="sites.txt"):
        self.domains_file = domains_file
        self.scraper = WPScraper()

    def get_domains(self, domains_file):
        with open(domains_file, 'r') as f:
            for line in f:
                yield line.strip()

    def check_domains(self):
        domains = self.get_domains(self.domains_file)
        domain_versions = []
        cur_v = self.scraper.get_current_version()

        wpscraper = self.scraper

        print('WordPress\' current version is: {}\n'.format(cur_v))

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.MAX_WORKERS
        ) as executor:
            future_domain = {
                executor.submit(wpscraper.get_domain_info, domain):
                domain for domain in domains
            }
            for future in concurrent.futures.as_completed(future_domain):
                domain = future_domain[future]
                print('[+]INFO: Checking {}...'.format(domain))

                try:
                    domain_scrape = future.result()
                except Exception as e:
                    print(
                        self.DANGER + '[!]ERROR: %r generated exception: %s %s'
                        % (domain, e, self.END)
                    )
                    continue

                if (
                        domain_scrape["version"] == False or
                        domain_scrape["title"] == False
                    ):
                    print(
                        self.WARN +
                        '[!]WARNING: Could not get title or version for %s %s'
                        % (domain, self.END)
                    )
                    continue

                #Get version dates as strings
                cur_v_date_str = self.scraper.get_version_date(cur_v)
                domain_v_date_str = self.scraper.get_version_date(
                    domain_scrape["version"]
                )
                # Clean up
                cur_v_date_str = cur_v_date_str.strip().replace(',','')
                domain_v_date_str = domain_v_date_str.strip().replace(',','')
                # Convert to datetime Object
                cur_v_date = datetime.strptime(cur_v_date_str, "%B %d %Y")
                domain_v_date = datetime.strptime(domain_v_date_str, "%B %d %Y")

                rounded_date = domain_v_date.replace(
                    hour = 0,
                    minute = 0,
                    second = 0,
                    microsecond = 0
                )
                delta = helpers.calc_days_diff(cur_v_date, domain_v_date)
                days_since = helpers.calc_days_diff(
                    datetime.now(),
                    domain_v_date
                )

                print(
                    "[+]INFO: %s version (%s) was released on %s"
                    % (domain, domain_scrape["version"], domain_v_date)
                )

                if delta >= 365:
                    status = 0
                    identifier = "!"
                elif delta >= 180:
                    status = 1
                    identifier = "+"
                else:
                    status = 2
                    identifier = "+"

                print(
                    versionstatus.get_colour(status) +
                    "\t [%s]UPDATE STATUS: %s (%d) %s"
                    % (
                        identifier,
                        versionstatus.get_status(status),
                        delta,
                        self.END
                    )
                )

                domain_info = {
                    "title": domain_scrape["title"],
                    "domain": domain,
                    "version": domain_scrape["version"],
                    "version_date": datetime.strftime(
                        domain_v_date,
                        "%b %d, %Y"
                    ),
                    "version_dist": delta,
                    "days_since": days_since,
                    "severity": versionstatus.get_status(status)
                }

                domain_versions.append(domain_info.copy())

        #Sort Values by days since last update
        sorted_values = sorted(
            domain_versions,
            key=itemgetter('days_since'),
            reverse=True
        )

        return sorted_values
