# OPPO Bắc Ninh – 20/10

Dự án Remotion hiện tại đã được cập nhật sang timeline Final No Thu Trang: **9 phút 03,783 giây**, đủ **51 ảnh nữ + 16 video lời chúc nam**, xuất **2560×1440 / 60 FPS / H.264 / AAC stereo**.

Xem [chi tiết thao tác bỏ duy nhất một ảnh và đồng bộ âm thanh](FINAL-NO-THU-TRANG.md). Bản gốc Final Polished được giữ để đối chiếu. Ảnh hiển thị đúng 6 giây/scene, crossfade 0,45 giây. Cấu trúc 4 nhóm: 13 / 13 / 13 / 12 ảnh → mỗi nhóm 4 lời chúc; giữ Intro; video 16 chuyển thẳng sang Outro gốc, đã bỏ toàn bộ closing-0 đến closing-3.

## Xuất nhanh trên GitHub

Mở **Actions → Render OPPO Final No Thu Trang 1440p60 → Run workflow → main**. Khi mọi bước render và QA xanh, tải artifact **OPPO-Bac-Ninh-20-10-Final-No-Thu-Trang-1440p60**. Artifact lưu 14 ngày, gồm MP4, preview, timeline và báo cáo kiểm tra. Mỗi lần cập nhật mã dựng/media trên `main` cũng tự chạy workflow.

## Chạy trên máy tính

Cài Node.js 22+, Python 3.12+, FFmpeg và font DejaVu hỗ trợ tiếng Việt. Cần MP4 Final Polished đã duyệt để giữ nguyên soundtrack; đặt `APPROVED_POLISHED_MP4` tới file đó (xem tài liệu ở trên). GitHub Actions tự tải artifact gốc của run `38909593711` khi artifact còn hạn.

```bash
npm ci
python3 -m pip install -r scripts/final/requirements.txt
npm run render:fast
npm run verify:render
```

Video: `out/oppo-bac-ninh-20-10-final-no-thu-trang-1440p60.mp4`.

Để xem bằng Remotion Studio:

```bash
npm run media:prepare
npm run media:stage
npm run studio
```

Composition `OppoBacNinh2010` dùng cùng scene đã dựng và cùng bản phối như đường FFmpeg, giữ nguyên hiệu ứng và bảng tên. `npm run render` cũng xuất cùng timeline qua Remotion. `npm run check` kiểm tra TypeScript/lint; `npm run build` tạo bundle.

## Media và biên tập

- `public/photos`: giữ 52 file ảnh gốc; chỉ 51 ảnh được render, loại `10_ĐINH THỊ THU TRANG.png`. Sắp xếp Unicode theo tên file; bỏ qua SVG mẫu. Giữ nguyên thiết kế và nội dung bằng contain, zoom nhẹ 94–99%.
- `public/videos/wishes`: đủ 16 video có số thứ tự 1–16; lấy tên/chức vụ trực tiếp từ tên file. Không thay tên file sau khi biên tập mà chưa cập nhật manifest.
- Intro: `public/videos/Intro.mp4`; Outro: `public/videos/Outro_20-10_OPPO_Bac_Ninh.mp4`.
- Nhạc ảnh: đúng `public/music/NHẠC 20.10.mp3`; nhạc Outro riêng: `public/music/Nhac outro.mp3`; nhạc intro: `public/music/abydos_music-opening-epic-logo-193120.mp3`.
- `src/data/speech-edits.json`: điểm vào/ra, tốc độ tối đa 1,10× giữ cao độ, phần lược bỏ và fingerprint nguồn. Khi nguồn đổi, bước chuẩn bị dừng để kiểm tra lại điểm cắt.
- `scripts/final`: kiểm kê → chuẩn bị layout → âm thanh → preview → render → QA. Tất cả 16 clip sau biên tập, gồm đệm hình/chuyển cảnh, đều dưới 18 giây.
- Giữ nguyên nhạc nền và ducking từ soundtrack Final Polished. Lệnh chuẩn bị hiện tại chỉ nối ngắn coda không lời; không chạy trình tạo nhạc hoặc xử lý lại giọng.

`public/generated`, `work`, `out`, `build` là kết quả tạo tự động, không đưa vào Git. Các script/scene 52 ảnh từ giai đoạn trước được giữ để tham chiếu; lệnh render và workflow mặc định chỉ dùng timeline Final No Thu Trang mới.
