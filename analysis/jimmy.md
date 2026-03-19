# 2025/04/24
簡先生 您好

今天總共蒐集三部桌機之硬碟映像檔及揮發性資料，且費用都已結清
跟針對側錄之網路封包進行來源去向IP初步分析，除了您的設備主動連線至外部網址還未有進一步確認之外，還有"6個外部IP連線到您的設備，以及由您的設備連線到3個外部IP"
這9個IP分別來自美國(1個)、英國(2個)、台灣(4個)、以及新加坡(2個)，其中有兩個連線進到您設備的IP已被列入惡意中繼站名單中，後續將會確認是否有相關的異常行為
以上簡短說明，若有問題再請跟我說，感謝!

# 2025/04/25
簡先生 您好

抱歉久等了，雖然我還沒有全部看完，但可針對目前發現的事項跟您做簡短的報告
先說明一下主機代稱，4/24當天進行三台主機的記憶體資料擷取以及第三台主機的網路封包側錄，依照擷取的先後順序，其主機名稱分別是MDJG3MI、4RCIOGN、MLQ5V4A(以下分別簡稱MDJ、4RC與MLQ)，其中的4RC即是您提到4/23才買的那台白色主機、MLQ即是最後有開啟網路側錄約1小時網路封包的那台座位旁電腦。

除了4RC可能因為沒接上網路(待確認)之外，另外兩部都有大量的網路連線IP紀錄，我總共分析了135個從這三部主機中取得之內外連線IP、比對了我之前取得的224個已知惡意中繼站IP之後，這三部主機確實有明顯遭到入侵的現象，您那天說的沒錯，MDJ那台電腦還蠻毒的。前述135個內外連線的IP中，共有11個已被列入惡意黑名單的IP(下方有整理表格)，通常有3個惡意外部IP已經是很明顯的外部入侵事件了......
這些IP實際上執行了什麼惡意行為我目前還未能全部看完，只能針對幾個部份跟您說明：

1. 就網路連線封包以及系統內的紀錄看來，您的電腦會透過VPN、Chrome以及Edge連線到外部惡意IP，以下節錄幾個畫面給您：
![alt text](image.png)
[截圖說明：這是在MDJ主機硬碟中的\ProgramData\NordVPN\configs\openvpn-config檔案，其中藍底的IP是已知惡意IP]


![alt text](image-1.png)
[截圖說明：這是在MDJ主機中的NordVPn日誌檔案]


![alt text](image-2.png)
[截圖說明：這是4RC主機的Google更新紀錄，其中藍底的IP也是已知惡意IP]

目前在這三部主機中找到的已知惡意IP清單如下：
IP
From
20.90.152.133
United Kingdom
103.172.41.121
Hong Kong
104.18.33.45
CloudFlare
185.213.82.138
Taiwan
13.107.42.16
United States
34.104.35.123 -
United States
52.123.128.14
United States
52.123.129.14
United States
150.171.27.10 -
United States
150.171.27.11 -
United States
150.171.28.10 -
United States

2. 在MLQ主機中有發現MDJ的IP，這部份需要先解釋一下，因4/24當天我到場的時候只有最後MLQ有接上網路線，這邊說的MDJ IP是從MDJ主機記憶體中擷取出來的封包檔案內發現的內部IP，分別是10.5.0.2、10.100.0.2、192.168.50.46。在下途中可以看到MLQ主機的某程式(應與NordVPN有關)之Gateway設定是MDJ主機。我不確定MLQ主機在不連接網路的狀態下，您如何安裝NordVPN(也可能不是您安裝的)，但或許是透過設定轉移、或從程式備份、或個人帳戶偏好等等的設定轉移到MLQ上，當然我還沒有排除攻擊者(目前看來應該是有的)透過區域網段或其他方法從MDJ主機跳到MLQ主機進行設定
![alt text](image-3.png)

3. 在分析惡意IP的過程中，發現MDJ主機有一些OpenVPN的日誌(也可能是執行歷程或設定檔)，如下圖，其中在[23:02:55.089]有c:\windows\system32\route.exe ADD 185.213.82.138這段文字，如之前所說，這個IP是來自台灣且已被列入黑名單的IP，所以我去找了這三部主機中所有的route.exe，共有45個一樣名稱的檔案，其中MDJ主機的route.exe檔案與其他兩部主機的完全不同；然而4RC和MLQ主機內部份的route.exe是完全一模一樣的，這代表著同樣的一些route.exe檔案在這兩部主機之間複製搬移的可能性。這些route.exe的檔案時間屬性有點複雜，我還沒整理完，但MDJ主機的route.exe相當簡單，想請問您今年4/1 17:35:31~17:35:42之間是否有讓MDJ主機連上網路? 還記得當天有做哪些動作嗎? 例如更新Windows或連線到VPN? 會這麼問是因為MDJ主機中所有的route.exe檔案最後存取時間都是前述那個時段，在我往下追查之前，希望有一些您對當天動作的說明，這樣我比較能釐清哪些可能是您操作的，哪些可能是系統自動做的，又有哪些可能是攻擊者做的
![alt text](image-4.png)

4. 您之前來信提到的cmd.exe，也是個值得追查的方向。三部主機內一共有79個cmd.exe(包括被刪除和複寫的)，其中有30種不同的cmd.exe(以HASH來區分，蠻多cmd.exe已經只剩下檔案名稱及路徑而算不出HASH)，這30個不同的HASH被Virustotal判定有5個cmd.exe具有中高風險(疑似惡意程式)的包裝方法，這5個cmd.exe分別在4RC(3個)、MDJ(1個)以及MLQ(2個)。尤其是MDJ的那個cmd.exe雖然沒有被防毒軟體判定為惡意程式，但風險較高(像是個木馬)，如下圖：
![alt text](image-5.png)

其他的cmd.exe也有中風險：
![alt text](image-6.png)


綜合上述，就目前的結果看來，攻擊者先入侵MDJ再跳到MLQ及4RC的路徑越來越清晰，以下是建議事項，希望能幫您改善現狀：
A. 開啟您之前採購的防火牆，內對外的部份將特定幾個一定會造訪的網站設定白名單(放行)、並將我前述的幾個已知惡意黑名單IP設定阻擋；外對內的部份則先設定阻擋所有來源，若發現必要且正常的網頁無法瀏覽，請確認防火牆日誌後再行開放。

B. 如前述中所提到，各設備可能存在彼此互相滲透攻擊，我建議將各主機的硬碟保留但不接上主機讀取。重新購置硬碟後，透過Windows安裝光碟重灌系統，並透過像是Revo uninstaller這類型的軟體將所有不會用到的Windows App(包括Edge)移除且刪除不必要的開機即執行程序(看得懂的不必要程式再刪除就好)。接著才連上網路，這時如果方便就請執行網路封包側錄(例如wireshark，我4/24當天在MLQ上執行的工具)，不方便封包側錄的話也請關注一下防火牆的阻擋日誌內容，看不出有不斷跳出連線需求(內外都要)失敗的情況後，再開始安裝Chrome(最好是在別的電腦中下載好。或由我這邊提供)以及其他軟體的安裝，最後才是開始瀏覽網頁頁面

C. 保留下來硬碟中的惡意程式(如果有)，可能會在您住所的環境中再次發作，如果一定要讀取的話，我會建議前題是將前述防火牆的設定處理好，並在硬碟接上電腦前開始進行網路封包側錄，這樣相對來說比較安全也比較能知道發生什麼事。

D. VPN的部份就請暫時別安裝，就前述的發現來看，裝了反而可能會被導向其他IP

以上說明，若有問題再請跟我說。未來一週我會著重在網頁行為分析、惡意程式關聯比對以及日誌紀錄內容確認等項目。

# 2025/06/05
簡先生 您好

抱歉最近感冒有點嚴重，耽擱分析進度了
有一些進度跟您更新，也有因為看到一些需要您協助部份再請您有空的時候回覆

根據之前看到可能有問題的cmd.exe，去做關聯比對，找到一個czg2fxp5.gll..exe，被放在20250424\DESKTOP-MLQ5V4A\E\Users\Yscpjkeaaon\AppData\Local\Temp\31b6f118-6ce5-4c4b-b39a-cb625c93244e\這個路徑底下，該路徑像是暫存下載檔案，但檔案名稱格式卻又不是，且從該檔案的雜湊值去查詢，得到NordVPNInstall.exe這個檔案名稱，也就是說Nordvpn這個程式跟前一封信找到的cmd.exe有關連
所以目前為止看到的線索，都指向Nordvpn有問題，接著攻擊者透過內部橫移，從MDJ跳到MLQ等另外兩台主機，以下是我在MLQ主機找到的其中一個證明

[20:14:17.855] [ERR] [72] [NetworkAdapterInformationService] Main network interface information is null. All adapters information Description: NordLynx Tunnel, Status: Up, Gateway: , IPAddress: 10.5.0.2;  Description: TAP-Windows Adapter V9, Status: Down, Gateway: , IPAddress: 169.254.145.28;  Description: OpenVPN Data Channel Offload, Status: Down, Gateway: , IPAddress: 169.254.12.151;  Description: TAP-NordVPN Windows Adapter V9, Status: Down, Gateway: , IPAddress: 169.254.64.207;  Description: Microsoft Wi-Fi Direct Virtual Adapter, Status: Down, Gateway: , IPAddress: 169.254.148.67;  Description: Microsoft Wi-Fi Direct Virtual Adapter #2, Status: Down, Gateway: , IPAddress: 169.254.135.49;  Description: Intel(R) Wi-Fi 6 AX201 160MHz, Status: Down, Gateway: , IPAddress: Not a private IP;  Description: Realtek PCIe GbE Family Controller, Status: Down, Gateway: , IPAddress: 169.254.32.237;  Description: Software Loopback Interface 1, Status: Up, Gateway: , IPAddress: Not a private IP;

需要您協助確認的問題有這些，如果時間久遠已經忘了當時的狀況也沒關係，我再看看有沒有其他線索：
1. 您在MDJ或其他兩台主機安裝NoedVPN的時間是否為2025/2/2 或 2025/3/17 或 2025/3/28? 會這樣問是因為這些日期都是部份cmd.exe被建立的時間，若都確認是您的安裝行為，我就可以把這些動作暫時列為白名單，繼續追查其他的線索
2. 在  DESKTOP-MDJG3MI\E\Users\ydnaa\AppData\Local\Google\Chrome\User Data\ZxcvbnData\3\這個路徑底下有個password.txt，內容看起來應該是一個破解密碼用的字典檔，請問這是您建立的嗎?
3. 我從日誌看來，有幾個主機登入的時間點需要確認是您、您家人抑或是可能的攻擊者，分別是
2022/01/01/週六 19:41:33 登入失敗
2025/03/08/週六 03:42:43 登入失敗
2025/03/08/週六 04:12:22 登入失敗
2025/03/11/週二 19:31:29 使用身份憑證登入成功
2025/03/11/週二 19:31:29 使用身份憑證登入成功
2025/03/11/週二 22:30:21 使用身份憑證登入成功
2025/03/11/週二 23:11:57 使用身份憑證登入成功
2025/03/12/週三 10:22:33 使用身份憑證登入成功

# 2026/01/05