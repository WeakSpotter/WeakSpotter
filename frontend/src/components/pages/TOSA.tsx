export default function TOSA() {
  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      <div className="card w-full max-w-4xl bg-white shadow-xl p-6">
        <div className="card-body">
          <h1 className="card-title text-2xl font-bold mb-4">
            Terms and Conditions of Use and Access
          </h1>
          <p>
            By accessing and using the website "WeakSpotter" (hereinafter
            referred to as "the Site"), as well as its hosted infrastructure,
            you acknowledge and agree to the following terms and conditions,
            which govern the use of security tools and tests performed on the
            Site.
          </p>

          <h2 className="text-xl font-semibold mt-4">
            1. Authorization of Security Tests
          </h2>
          <p>
            You expressly authorize "WeakSpotter" and its infrastructure to
            perform, without limitation, the following security tests on the
            Site and its associated systems:
          </p>
          <ul className="list-disc list-inside ml-4">
            <li>
              <strong>Nikto</strong>: Vulnerability scanner for web servers.
            </li>
            <li>
              <strong>ZAPIT</strong>: Proxy for detecting vulnerabilities in web
              applications.
            </li>
            <li>
              <strong>Wapiti</strong>: Web vulnerability scanner analyzing web
              applications to identify security flaws.
            </li>
            <li>
              <strong>Sublist3r</strong>: Tool for enumerating subdomains via
              search engines and other sources.
            </li>
            <li>
              <strong>SSH-Audit</strong>: Tool for auditing SSH server
              configurations and versions.
            </li>
            <li>
              <strong>Oralyser</strong>: Tool for analyzing and collecting
              information on DNS registries and records.
            </li>
            <li>
              <strong>Nmap</strong>: Port scanner for discovering hosts and
              services on a computer network.
            </li>
            <li>
              <strong>Harvester</strong>: Automatic extraction of email
              addresses from public sources.
            </li>
            <li>
              <strong>CMSmap</strong>: Vulnerability scanner for content
              management systems (CMS).
            </li>
            <li>
              <strong>HTTP</strong>: Protocol for web communication.
            </li>
            <li>
              <strong>Whois</strong>: Service for querying domain registration
              information.
            </li>
            <li>
              <strong>Record</strong>: Analysis of specific entries in a DNS
              zone file (A, MX, TXT, etc.).
            </li>
            <li>
              <strong>Domain</strong>: Analysis of the domain name identifying
              the Site.
            </li>
            <li>
              <strong>Cloudflare</strong>: Use of the content delivery network
              and DDoS protection service.
            </li>
            <li>
              <strong>WPScan</strong>: Tool for analyzing vulnerabilities in
              WordPress sites.
            </li>
            <li>
              <strong>Vulnx</strong>: Vulnerability scanner primarily targeting
              CMS and other web applications.
            </li>
            <li>
              <strong>Joomscan</strong>: Vulnerability scanner for websites
              using Joomla (CMS).
            </li>
            <li>
              <strong>Droopescan</strong>: Tool for analyzing vulnerabilities in
              websites using Drupal, SilverStripe, WordPress, and Joomla CMS.
            </li>
          </ul>

          <h2 className="text-xl font-semibold mt-4">
            2. Ownership and Responsibility
          </h2>
          <p>
            You declare that you are the legitimate owner of the Site and the
            machine on which it is hosted. You assume full responsibility for
            the consequences arising from the tests performed, including but not
            limited to, service interruptions, configuration changes, or
            indirect damages.
          </p>

          <h2 className="text-xl font-semibold mt-4">
            3. Non-Banning of IP Addresses
          </h2>
          <p>
            You agree not to permanently or temporarily ban, block, or restrict
            the IP addresses used by "WeakSpotter" as part of the security
            tests. This commitment includes, but is not limited to, IP addresses
            associated with the security tools mentioned above.
          </p>

          <h2 className="text-xl font-semibold mt-4">
            4. Non-Reporting of IP Addresses
          </h2>
          <p>
            You agree not to report, disclose, or share the IP addresses used by
            "WeakSpotter" or its infrastructure with third parties, including,
            but not limited to, competent authorities, internet service
            providers, or legal entities, except in cases of proven and manifest
            violation of applicable laws. This commitment includes, but is not
            limited to, IP addresses associated with the security tools
            mentioned in these terms.
          </p>
          <p>
            By accepting these terms, you acknowledge and agree that the
            activities carried out by "WeakSpotter" as part of the security
            tests are conducted at your request and with your express
            authorization. Consequently, you waive any claim, lawsuit, or legal
            action against "WeakSpotter," its owners, employees, partners, or
            affiliates, for any direct or indirect consequences resulting from
            the use of IP addresses associated with the security tests.
          </p>

          <h2 className="text-xl font-semibold mt-4">
            5. Limitation of Liability
          </h2>
          <p>
            "WeakSpotter" disclaims all liability for direct, indirect, or
            consequential damages resulting from the use of the security tools
            mentioned above. You agree to indemnify and hold "WeakSpotter"
            harmless from any claim, loss, or damage arising from these tests.
          </p>

          <h2 className="text-xl font-semibold mt-4">
            6. Modification of Terms
          </h2>
          <p>
            "WeakSpotter" reserves the exclusive right to modify, update, or
            supplement these terms and conditions at any time, without prior
            notice. These modifications may include, but are not limited to,
            adjustments related to the evolution of security tools used, changes
            in operational practices, or updates to comply with legal or
            regulatory requirements.
          </p>
          <p>
            Any changes to the terms will take effect immediately after their
            publication on the Site or after direct notification to the user, as
            determined by "WeakSpotter." It is your responsibility to regularly
            review the terms and conditions to stay informed of any changes.
          </p>
          <p>
            By continuing to use the Site and its infrastructure, you agree to
            be bound by these terms and conditions. If you do not accept these
            terms, you must immediately cease all use of the Site and its
            services.
          </p>
        </div>
      </div>
    </div>
  );
}
