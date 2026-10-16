# OPPO Bắc Ninh — Video 20/10 (giai đoạn 2)

Remotion + React + TypeScript, **2560 × 1440, 60 fps, H.264 / yuv420p**.
Dữ liệu lấy từ main tại commit `8961206`: 52 thiệp nhân sự thật, nhạc MP3 và hai clip.

## Xem trước

Cài Node.js 22 trở lên (bản LTS), tải repository về máy và mở Terminal trong thư mục dự án:

```bash
npm ci
npm run studio
```

Mở URL Studio in ra, thường là http://localhost:3000, chọn `OppoBacNinh2010`.
Các composition `Intro`, `Slideshow`, `Outro` xem riêng từng phần.

## Xuất video chất lượng cao

```bash
npm run render
```

Lệnh tự kiểm kê media, kiểm tra TypeScript/ESLint rồi render. Kết quả:

```text
out/oppo-bac-ninh-20-10-1440p60.mp4
```

Nhấn chuột phải file MP4 trong thư mục `out` để sao chép/chia sẻ. Không cần cài FFmpeg riêng;
Remotion có bộ công cụ FFmpeg đi kèm. Lần đầu Remotion có thể tải Chrome.
Nếu máy đã cài Chromium và muốn sử dụng:

```bash
npm run render -- --browser-executable=/usr/bin/chromium --concurrency=2
```

MP4 dùng CRF 16, H.264, âm thanh AAC stereo 320 kbps. Hai clip nguồn là 30 fps;
chúng giữ nguyên tốc độ/thời lượng, được đặt trên timeline 60 fps. Ảnh/hiệu ứng chạy ở 60 fps.
Đầu ra lớn hơn kích thước ảnh gốc; không dùng AI để sửa khuôn mặt hoặc nội dung.

## Tải MP4 từ GitHub, không cần cài trên máy

Vào tab **Actions** → **Render OPPO 20-10 video** → chọn lượt chạy có dấu tích xanh.
Cuối trang, bấm artifact **OPPO-Bac-Ninh-20-10-1440p60**, tải ZIP và giải nén để lấy MP4.
Cần đăng nhập GitHub để tải artifact. Artifact lưu 14 ngày; có thể bấm **Run workflow**
để xuất lại. Workflow chỉ tải lên kết quả sau khi kiểm tra MP4 thành công.
Workflow chạy khi cập nhật media/mã dựng trên main hoặc khi bấm **Run workflow**.
Khi chạy thủ công, chọn nhánh **main** để dùng mã mới nhất.

## Media và thứ tự

- `public/photos/`: đúng 52 file PNG/JPG/WebP; bỏ qua 3 SVG mẫu và `.gitkeep`.
- Sắp tăng dần **theo nguyên tên file Unicode**, bao gồm tiền tố 01–10; không dùng thứ tự tải lên hoặc số thứ tự làm khóa duy nhất.
- Mỗi file xuất hiện đúng một lần. Các tiền tố trùng số vẫn là những ảnh riêng biệt.
- `public/music/NHẠC 20.10.mp3`: khớp chính xác dấu tiếng Việt và dấu cách.
- `public/videos/Intro.mp4`: 8,3 giây, giữ nguyên toàn bộ clip.
- `public/videos/Outro_20-10_OPPO_Bac_Ninh.mp4`: 20 giây, giữ nguyên toàn bộ clip.
- Hai ảnh `NGUYỄN THỊ VUI.webp` và `TRẦN THỊ LINH.jpg` chứa dữ liệu PNG: giữ nguyên file gốc và tên, đã kiểm tra giải mã thực tế.

`npm run media:prepare` đọc các file thực tế, kiểm tra đủ 52 ảnh, SHA-256 không trùng,
đọc thời lượng bằng FFprobe rồi tạo `src/data/media-manifest.json` và `work/photo-timeline.csv`.
Không sửa manifest thủ công. Chương trình sẽ dừng nếu thiếu/thừa ảnh hoặc sai tên nhạc.

## Trình chiếu

Video dài **253,15 giây / 15.189 frame**. Nhạc chạy một lượt xuyên suốt, không lặp,
không tăng/giảm tốc; fade-in 1,5 giây, fade-out 3 giây, âm lượng 85%.
Hai video nguồn không có track âm thanh; cấu hình vẫn đặt `muted` để tránh trộn âm ngoài ý muốn.

Mỗi thiệp dài 302 hoặc 303 frame (khoảng 5,03–5,05 giây), crossfade 42 frame (0,7 giây).
Cân bằng số frame lẻ giúp khớp nhạc, không tích lũy sai số hoặc thêm cảnh lặp ở cuối.
Ảnh hiển thị nguyên tấm bằng `contain`; zoom in/zoom out luân phiên 94%–99%, easing smoothstep chậm ở đầu/cuối,
giữ trọn bốn mép và toàn bộ tên, chân dung, lời chúc. Không có chữ mới đè lên ảnh.
Ánh sáng quét và lấp lánh nhẹ, chuyển động tính theo frame.

## Xuất nhanh trên máy ít CPU

Đường xuất này cần **FFmpeg bản đầy đủ** trong PATH (kiểm tra bằng `ffmpeg -version`).
Trên macOS có Homebrew: `brew install ffmpeg`; trên Windows: `winget install Gyan.FFmpeg`;
sau khi cài, mở Terminal mới. Nếu không muốn cài FFmpeg, dùng `npm run render`
hoặc tải artifact GitHub theo hướng dẫn phía trên.

```bash
npm run render:fast
```

Đường xuất này dùng FFmpeg với cùng manifest 52 ảnh và cùng số frame, clip, nhạc,
zoom an toàn, ánh sáng quét, lấp lánh, crossfade. H.264 CRF 16 / preset fast,
AAC 320 kbps, 1440p60; kết quả vẫn ở đường dẫn `out/` nêu trên.
Đây là đường xuất dùng cho MP4 được bàn giao trong môi trường cloud.
Remotion Studio và `npm run render` vẫn là đường xem trước/render qua trình duyệt;
cách vẽ ánh sáng, lấp lánh và nền của hai bộ xuất có khác biệt nhẹ.
Các clip trung gian được cache trong `work/native-*` để chạy tiếp khi bị gián đoạn.
Phần chuyển cảnh dùng bộ trộn ảnh tích hợp và điều khiển opacity theo từng frame bằng smoothstep; đầu/cuối dịu hơn, giữ nguyên crossfade 42 frame và toàn bộ thời lượng.

## Kiểm tra

```bash
npm run check
npm run build
npm run verify:render
```

`build` chỉ biên dịch, không xuất MP4. `verify:render` chạy sau khi có MP4:
kiểm tra codec/kích thước/60 fps/số frame, giải mã toàn bộ hình và âm thanh,
đối chiếu khung hình giữa cả 52 cảnh với 52 ảnh gốc để phát hiện thiếu/lặp/sai thứ tự,
đối chiếu intro/outro, kiểm tra tương quan nhạc và fade âm thanh.
Báo cáo ở `work/qa-report.json`; thumbnail kiểm tra ở `work/qa/`.
Có thể truyền đường dẫn khác: `npm run verify:render -- /duong-dan/video.mp4`.

## Cấu trúc chính

```text
scripts/prepare-media.mjs     Kiểm kê nguồn, thời lượng, hash và thứ tự ảnh
scripts/verify-render.mjs     Kiểm tra MP4 đã xuất
scripts/render-native.mjs     Xuất FFmpeg từ cùng timeline, hỗ trợ chạy tiếp
src/data/media-manifest.json  Dữ liệu và timeline sinh từ media thật
src/OppoVideo.tsx             Intro → 52 ảnh → Outro, nhạc xuyên suốt
src/scenes/PhotoScene.tsx     Nguyên thiệp, zoom an toàn, ánh sáng
src/scenes/MediaClips.tsx     Hai clip Intro/Outro thật
src/scenes/Slideshow.tsx      Crossfade đủ 52 ảnh
src/Root.tsx                 Các composition 1440p60
src/data/motion.json         Biên độ zoom dùng chung, không đổi media/timeline
src/motion.ts                Đường cong chuyển động trong Remotion
scripts/motion.mjs           Cùng đường cong cho FFmpeg và kiểm tra MP4
```

Các scene chữ và cấu hình `content.ts`/`timing.ts` của giai đoạn 1 được giữ làm tham khảo;
video giai đoạn 2 dùng `media-manifest.json`. Không cần nhập lại tên và lời chúc.
`out/`, `build/`, `work/`, `node_modules/` không được commit. MP4 không đưa vào Git history.
