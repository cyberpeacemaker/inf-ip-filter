To check for untrusted or rogue certificates, we need to look into the **Trusted Root Certification Authorities** store. This is the "VIP list" of entities your computer trusts to verify the identity of websites. If an attacker's name is on this list, they can impersonate any HTTPS site without your browser throwing a warning.

Here is how to audit your certificates on Windows and Mac.

---

## On Windows (Certificate Manager)

Windows stores certificates in a central repository that Chrome, Edge, and Brave all use.

1. Press **Win + R**, type `certmgr.msc`, and hit Enter.
2. In the left pane, click on **Trusted Root Certification Authorities** and then double-click the **Certificates** folder inside it.
3. **What to look for:**
* Look at the **"Issued To"** and **"Issued By"** columns. Usually, these should be recognizable names like *DigiCert, Sectigo, GlobalSign, Microsoft,* or *Amazon*.
* **Red Flags:** Any certificate that has a generic name (e.g., "Root," "Monitor," "Default"), your own PC's name, or a name related to a "Search Assistant" or "Ad-Blocker" you don't recognize.


4. **Right-click and Delete** any certificate that looks suspicious (though be careful; deleting a legitimate one can break some apps).

---

## On macOS (Keychain Access)

Macs use the Keychain to manage trust.

1. Open **Keychain Access** (Command + Space, type "Keychain Access").
2. Select **System Roots** in the left sidebar and click the **Certificates** tab.
3. Look for any certificate with a **blue circle with a white plus sign (+) or a red X**. This indicates the trust settings have been manually modified.
4. **The "Profiles" Check:** This is even more important for Mac users. Go to **System Settings > Privacy & Security > Profiles** (at the very bottom).
* **If you see a profile you didn't install** (often named "Admin Settings" or "Chrome Config"), this is almost certainly how the hijacker is forcing the Bing redirect and injecting certificates. Delete the profile immediately.



---

## On Chrome/Edge Directly

You can also see what the browser specifically sees:

1. Open Chrome/Edge settings and search for **"Manage Certificates."**
2. Go to the **Authorities** tab.
3. Scroll through the list. If you see an entry that doesn't belong to a major tech company or security firm, it’s worth investigating.

---

### What to do if you find one

If you find a suspicious certificate:

1. **Export it first** (just in case you need to see what it was later).
2. **Delete/Remove** it.
3. **Restart your browser.** If the "Bing" redirect stops, or if you suddenly start getting "Privacy Warnings" on sites, you've found the "Man-in-the-Middle" tool the malware was using.

### A Note on "SSL Inspection"

Some legitimate antivirus programs (like Avast or Bitdefender) install their own root certificates to scan encrypted traffic for viruses. If you see a certificate issued by your antivirus, that is usually normal—though it technically uses the same "MITM" technique as the hijackers!

**Would you like me to show you how to check your "Hosts" file next? This is another common place where hijackers redirect your traffic at the system level.**