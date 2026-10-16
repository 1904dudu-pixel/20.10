# OPPO Bắc Ninh – Gửi một nửa yêu thương | Final Polished

Timeline mới: **09:09.333**, **32960 frame**, 75 cảnh. Đầu ra H.264 CRF 17, 2560×1440, 60 FPS; AAC stereo 48 kHz 320 kb/s.

Bản này tiếp tục dự án đã duyệt dài 09:26.333. Toàn bộ 52 ảnh, thứ tự nhân sự, thời lượng ảnh 6 giây, hiệu ứng và 16 đoạn cắt lời nói/tốc độ đã duyệt được giữ nguyên. Mốc cũ trước phần closing vẫn là mốc mới; chỉ Outro dời sớm 17 giây.

## 1. Bảng tên 16 nhân sự

Giữ bố cục, nền xanh OPPO đậm bán trong suốt, tên trắng và chức vụ champagne. Hiệu ứng đi từ dưới lên/fade và cửa sổ hiện 3,75 giây giữ nguyên; bảng tên nằm ngoài vùng video người nói. Chức vụ người số 1 đã được người dùng xác nhận là **GIÁM ĐỐC KINH DOANH**.

| # | Tên hiển thị | Chức vụ | Bắt đầu scene | Thời lượng scene |
|---|---|---|---|---|
| 1 | Anh. NGUYỄN CÔNG HƯNG | GIÁM ĐỐC KINH DOANH | 01:25.067 | 17.78s |
| 2 | Anh. TRẦN TUẤN HƯNG | SALE LEADER | 01:42.400 | 14.20s |
| 3 | Anh. PHAN ĐÌNH QUYỀN | SALE LEADER | 01:56.150 | 12.80s |
| 4 | Anh. NGUYỄN KINH TUẤN | SALE LEADER | 02:08.500 | 17.53s |
| 5 | Anh. LƯU VĂN BÁCH | IOT LEADER | 03:39.783 | 16.35s |
| 6 | Anh. NGUYỄN THẾ DUY | TRAINER | 03:55.683 | 9.55s |
| 7 | Anh. NGÔ VĂN THÁI | TRAINER | 04:04.783 | 7.20s |
| 8 | Anh. ĐÀO ĐĂNG THÙY | SALE BẮC GIANG | 04:11.533 | 13.37s |
| 9 | Anh. LƯƠNG VĂN TUẤN | SALE BẮC GIANG | 05:38.650 | 15.50s |
| 10 | Anh. NGUYỄN THẠC TÙNG | SALE BẮC NINH | 05:53.700 | 14.15s |
| 11 | Anh. NGUYỄN THẾ ANH | SALE LẠNG SƠN | 06:07.400 | 17.55s |
| 12 | Anh. NGUYỄN TRƯỜNG GIANG | SALE HƯNG YÊN | 06:24.500 | 17.58s |
| 13 | Anh. TRIỆU VIẾT HƯỚNG | SALE BẮC GIANG | 07:55.833 | 13.25s |
| 14 | Anh. VŨ THẾ DUY | SALE LẠNG SƠN | 08:08.633 | 14.95s |
| 15 | Anh. NGUYỄN VĂN LƯƠNG | PB BẮC NINH | 08:23.133 | 11.75s |
| 16 | Anh. PHẠM VĂN TÙNG | PB BẮC NINH | 08:34.433 | 15.35s |

Mỗi scene lời chúc vẫn dưới 18 giây. Tên/chức vụ nguồn trong tên file vẫn được lưu riêng; chỉ thông tin hiển thị có tiền tố và chức vụ số 1 được cập nhật.

## 2. Sửa vùng nhạc 05:28–05:35

Bài hát trước đây kết thúc tại **05:28.880**, khi ảnh còn hiển thị. Đã mở rộng đoạn nguồn từ 138,72–202,90s thành **138,72–211,18s**, đến hết câu/đoạn hát tiếp theo. Crossfade **336.610–337.160s** (05:36.610–05:37.160), dài 0,55 giây.
Ảnh cuối của nhóm kết thúc tại **05:37.050**; lời nói nam đầu tiên bắt đầu tại **05:39.100**. Nhạc hát vì thế đi hết phần ảnh; instrumental tiếp nhận tại bảng dẫn trước người nói, rồi tự hạ dưới giọng nói. Hai nhóm nhạc đầu giữ nguyên.

## 3. Điệp khúc cao trào

Đoạn nguồn **199.68–223.26s** của `public/music/NHẠC 20.10.mp3`, dài **23.58s**, phát tại **07:31.000–07:54.580** trong timeline mới. Giữ trọn các câu hát đến hết điệp khúc, không đổi tốc độ.

Đã so sánh ba đoạn điệp khúc tương ứng: RMS 0,17610 / 0,17550 / **0,18582**. Chọn lần cuối có năng lượng đều cao hơn và còn đủ headroom. Fade-in/out 0,8 giây. Đoạn lặp đi vào phần đuôi gần im của bài gốc, tránh hai câu hát chồng nhau. Fade-out bắt đầu tại **07:53.780**, sát bảng dẫn nhóm 4 (**07:53.783**); câu hát kết thúc **07:54.580**, trước lời nói video 13 tại **07:56.283**. Không đổi, lặp hoặc đảo ảnh.

## 4. Xóa toàn bộ bốn closing

**Đã bỏ hoàn toàn `closing-0`, `closing-1`, `closing-2`, `closing-3` khỏi timeline và bước tạo đồ họa. Không chuyển bốn đoạn chữ sang nơi khác và không thêm cảnh thay thế.**

Cụm closing của bản cũ đóng góp **17,000 giây** sau khi tính các overlap; xóa theo cấu trúc scene đúng yêu cầu mới nhất, thay vì chỉ cắt máy móc 14 giây ở giữa cụm.
Lời chúc của **Anh. PHẠM VĂN TÙNG** bắt đầu tại **08:34.433** và giữ nguyên toàn bộ đoạn nói đã duyệt. Giọng nói kết thúc tại **08:49.333**. Chuyển thẳng sang **Outro gốc** tại **08:49.333**, crossfade hình **0,45 giây**; không có scene trung gian. Outro kết thúc tại **09:09.333**.

Chữ và hiệu ứng vốn có bên trong file video Outro gốc được giữ nguyên theo yêu cầu, không thêm lớp lời chúc mới.

## 5. Nhạc Outro riêng

**Đã tìm thấy đúng `public/music/Nhac outro.mp3`** (33,456 giây theo container; khoảng 33,362 giây giải mã). Video `Outro_20-10_OPPO_Bac_Ninh.mp4` dài đúng **20 giây**, không có stream âm thanh gốc; video được xuất ở tốc độ 1,00×, không cắt và không đổi thiết kế.
Chọn nguồn nhạc **11.40–31.60s**: giữ trọn câu hát cuối về OPPO Bắc Ninh, nhạc cao trào và nhịp kết có đuôi vang tự nhiên. Nhạc có tiền âm **0,20 giây** từ **08:49.133**; ở frame đầu Outro, nguồn nhạc đang ở **11,60s**. Fade-in 0,25 giây, fade-out cuối 0,30 giây, không time-stretch.

Điểm nhấn nguồn 14,132s → video Outro 02,532s (tên OPPO Bắc Ninh đang đi vào khung); 16,002s → 04,402s (tiêu đề đang xuất hiện); nhịp kết 29,372s → 17,772s, tiếp theo là đuôi vang tới khi video kết thúc. Giữ nguyên ánh sáng/bokeh sang trọng đã có trong video gốc.
Nhạc instrumental của phần nam fade 0,45 giây trước Outro và bằng **0** từ **08:49.333** trở đi. Phần tiền âm Outro không có lời hát đè lên câu chúc cuối.

## Preview và kiểm tra

- `01-labels.mp4`: bảng tên đầu tiên với chức vụ đã xác nhận; `labels-contact.jpg`: đủ 16 bảng tên.
- `02-music-transition.mp4`: 05:25–05:42.
- `03-chorus-reprise.mp4`: 07:29–07:58.
- `04-direct-outro.mp4`: video 16 và toàn bộ Outro gốc trong timeline mới.

Preview kiểm tra số frame, H.264 60 FPS, AAC stereo, đối chiếu âm thanh với bản phối và giải mã toàn bộ. Chỉ sau khi preview/preflight đạt mới render toàn bộ. Kiểm tra cuối đối chiếu khung của cả 75 scene, 16 giọng nói, số frame, true peak, hình đen, khoảng mất tiếng và giải mã toàn bộ MP4. Báo cáo thực tế nằm trong artifact, không coi báo cáo preflight là bằng chứng render thành công.

## Render và lấy file

```bash
npm ci
python3 -m pip install -r scripts/final/requirements.txt
npm run render:fast
npm run verify:render
```

Cần Linux/WSL2 với Node.js 22+, Python 3.12+, FFmpeg và `fonts-dejavu-core`. Để xem Studio: `npm run media:prepare`, `npm run media:stage`, `npm run studio`. Composition `OppoBacNinh2010` tự lấy timeline mới từ manifest và dùng cùng scene/bản phối như đường xuất nhanh.

MP4: `out/oppo-bac-ninh-20-10-final-polished-1440p60.mp4`. GitHub Actions: **Render OPPO Final Polished 1440p60**. Artifact: **OPPO-Bac-Ninh-20-10-Final-Polished-1440p60**, lưu ít nhất 14 ngày. Bên trong có MP4, bốn preview, contact sheet bảng tên và hình ảnh, timeline, báo cáo preflight, preview, âm thanh và QA.
