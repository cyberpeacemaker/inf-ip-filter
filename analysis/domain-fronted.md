Here is a **clean, structured version** of your text with clearer formatting and organization:

---

# Domain Fronting

**Domain fronting** is an Internet censorship-circumvention and threat-actor technique that hides the true destination of HTTPS traffic. By using a reputable **“front” domain** in the TLS **Server Name Indication (SNI)** and a blocked or malicious domain in the encrypted HTTP header, the traffic can bypass filters because the initial connection appears legitimate.

---

## Key Aspects of Domain Fronting

### Mechanism

Domain fronting relies on **Content Delivery Networks (CDNs)** or shared hosting environments where multiple websites share a single TLS certificate.

* A **visible, benign domain** is used during the TLS handshake.
* The **actual destination** is revealed only after encryption has been established.

---

### Components

**1. Front Domain (SNI)**

* The benign domain visible to network inspectors
* Example: `trusted.com`

**2. Hidden Host (HTTP Header)**

* The real destination specified in the encrypted HTTP request
* Example: `blocked-site.com`

---

### Purpose

**Circumvention**

* Allows users in censored regions to access blocked websites.

**Malicious Use**

* Threat actors may disguise **Command-and-Control (C2)** traffic as normal web browsing.

---

### Detection & Mitigation

While domain fronting can be effective, major cloud providers have taken steps to restrict it.

**Mitigation efforts include:**

* Blocking mismatched host headers
* Enforcing stricter CDN routing policies

**Detection methods include:**

* **Deep Packet Inspection (DPI)**
* **SSL/TLS inspection**
* Checking whether the **SNI matches the HTTP Host header**

Major providers such as **Amazon**, **Google**, and **Cloudflare** have implemented protections to reduce the abuse of domain fronting.

---

## Technical Workflow

1. **DNS Request / TLS Handshake**

   * The client connects to `trusted.com` (a CDN IP).

2. **Encrypted Tunnel Creation**

   * A secure HTTPS connection is established.

3. **HTTP Request Inside Tunnel**

   * The client sends a request specifying

     ```
     Host: blocked-site.com
     ```

4. **CDN Routing**

   * The CDN decrypts the request, reads the HTTP header, and routes the request to `blocked-site.com`.

---

## Why It Works

Blocking the hidden destination would require censors to block the **entire CDN infrastructure**, which could disrupt many legitimate services and cause significant **collateral damage**.

---

If you want, I can also:

* Turn this into **exam notes / cheat sheet format**,
* Make a **visual diagram of the domain fronting workflow**, or
* Convert it into **cybersecurity report style**.
