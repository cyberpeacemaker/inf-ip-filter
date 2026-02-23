To see exactly which DLLs (Dynamic Link Libraries) Microsoft Edge is running and check them against VirusTotal, the best tool is **Process Explorer** (part of Microsoft’s own Sysinternals suite). It is much more powerful than the standard Task Manager for this specific task.

---

## 1. Download & Set Up Process Explorer

Since this is a portable tool from Microsoft, you don't need to install it.

1. Download **[Process Explorer](https://learn.microsoft.com/en-us/sysinternals/downloads/process-explorer)**.
2. Right-click `procexp.exe` and select **Run as Administrator** (this is required to see deep system DLLs).

## 2. Enable VirusTotal Integration

Process Explorer has a built-in feature that sends the "digital fingerprint" (hash) of every file to VirusTotal automatically.

1. Go to the **Options** menu at the top.
2. Select **VirusTotal.com** > **Check VirusTotal.com**.
3. Accept the Terms of Service.
4. You will now see a new **VirusTotal** column. If you see numbers like `0/76`, it means 0 out of 76 antivirus engines flagged it. If you see **red numbers** (e.g., `5/76`), click the number to see exactly which engines found a problem.

---

## 3. How to See Edge’s DLLs

By default, you only see the `.exe` files. To see the DLLs inside them:

1. Find `msedge.exe` in the list (Edge usually has many sub-processes; pick the main one at the top of the tree).
2. Press **Ctrl + D** on your keyboard (or go to **View > Lower Pane View > DLLs**).
3. The window will split. The bottom half now lists every single DLL that Edge is currently using.

### How to Audit the DLL List

In that bottom pane, look for these specific red flags:

* **The VirusTotal Column:** If any DLL in that bottom list has a high detection ratio (red text), it’s likely your hijacker.
* **Company Name:** Sort by the "Company Name" column. Most should say **Microsoft Corporation**. If you see a DLL with *no* company name or a strange name (e.g., "Great Search Ltd"), right-click it and select **Check VirusTotal**.
* **Path:** Legitimate Edge DLLs are usually located in `C:\Program Files (x86)\Microsoft\Edge`. If you see a DLL being loaded from `C:\Users\YourName\AppData\Local\...` or a `Temp` folder, that is highly suspicious.

---

## 4. Manual Check (The "Old School" Way)

If you find a specific file and want to be 100% sure:

1. In Process Explorer, right-click the suspicious DLL in the bottom pane.
2. Select **Properties**.
3. Copy the **Path** of the file.
4. Go to **[VirusTotal.com](https://www.virustotal.com)** in your browser.
5. Upload that specific `.dll` file directly. This is more thorough than a hash check because it analyzes the file's behavior.

---

### Pro Tip: Verify Signatures

In Process Explorer, go to **Options > Verify Image Signatures**. This will add a "Verified" column. If a DLL says **"(Unverified)"**, it means the code hasn't been digitally signed by Microsoft or a trusted vendor—this is the #1 way to spot tampered DLLs.

**Would you like me to help you interpret a specific result if you find a DLL that looks suspicious?**