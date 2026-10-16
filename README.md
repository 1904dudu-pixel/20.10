# OPPO Bắc Ninh — Chúc mừng 20/10

Dự án Remotion + React + TypeScript dựng video chúc mừng Ngày Phụ nữ Việt Nam.
Giai đoạn 1 cung cấp mã nguồn hoạt động với ba ảnh SVG minh họa tự tạo, chưa có nhạc thật và chưa xuất MP4.

## Thông số và thiết kế

- Ngang 16:9, **2560 × 1440**, 30 fps.
- Bản mẫu **31,8 giây / 954 frame**: intro, ba cảnh ảnh và outro.
- Nền kem, xanh ngọc OPPO, điểm nhấn vàng và hoa hồng phấn.
- Lời chúc đi từ dưới lên, ảnh zoom nhẹ, ánh sáng lấp lánh và crossfade 0,8 giây.
- Toàn bộ animation chạy theo frame; không phụ thuộc thời gian thực hay ảnh/font từ Internet.
- Nhạc nền tùy chọn có lặp, fade-in 1,5 giây và fade-out 2 giây; mặc định tắt.

## Cài đặt và xem trước

Yêu cầu Node.js **22 trở lên**, npm và Git. Chạy từ thư mục gốc repository:

```bash
npm ci
npm run studio
```

Mở URL mà Studio in ra (thường là `http://localhost:3000`), chọn **OppoBacNinh2010**.
Trong thư mục **Scenes** có Intro, Slideshow, Outro để xem riêng từng phần.
Studio tự cập nhật khi lưu mã nguồn.

```bash
npm run check         # TypeScript + ESLint
npm run build         # Biên dịch bundle vào build/, không xuất video
npm run compositions  # Xác thực và liệt kê composition bằng Chromium
```

Lệnh `compositions` cần trình duyệt: Remotion có thể tải Chrome ở lần chạy đầu.
Nếu máy đã có Chromium, có thể chỉ định đường dẫn:

```bash
npm run compositions -- --browser-executable=/usr/bin/chromium
```

## Thay ảnh và lời chúc

1. Chép ảnh vào `public/photos/`, ví dụ `public/photos/chi-lan.jpg`.
2. Mở `src/data/content.ts`, sửa mảng `photos`:

```ts
export const photos: Photo[] = [
  {
    src: 'photos/chi-lan.jpg',
    name: 'Chị Lan',
    caption: 'Chúc chị luôn rạng rỡ,\nhạnh phúc và thành công!',
    objectPosition: 'center 30%',
  },
  // Thêm ảnh khác tại đây.
];
```

`src` là đường dẫn tương đối trong `public/`, không thêm tiền tố `public/` hay dấu `/` đầu.
Ảnh dọc được hiển thị trong khung vòm theo `object-fit: cover`; dùng `objectPosition`
để điều chỉnh vị trí khuôn mặt. Ảnh ngang cũng dùng được nhưng sẽ bị cắt hai bên.
Nên dùng JPG/PNG/WebP đủ lớn và tên file đơn giản.

Thêm/bớt ảnh sẽ tự cập nhật thời lượng. Nếu mảng rỗng, video vẫn chạy với một cảnh lời chúc.
Để giữ bố cục thoáng, nên dùng tên/tiêu đề ngắn, lời chúc khoảng hai dòng như mẫu.
Sửa object `content` cùng file để thay tên đơn vị, intro, outro và chữ ký.
Ký tự `\n` tạo dòng mới trong lời chúc.

## Thêm nhạc sau này

Chép file nhạc vào `public/music/`, rồi sửa `music` trong `src/data/content.ts`:

```ts
export const music: {src: string | null; volume: number} = {
  src: 'music/nhac-nen.mp3',
  volume: 0.35,
};
```

Giữ `src: null` để chạy không có nhạc. Âm lượng thường từ `0` đến `1`.
Nhạc ngắn sẽ tự lặp; fade-out luôn đi theo thời lượng video hiện tại.

## Chỉnh thời lượng và phong cách

`src/timing.ts` điều khiển số giây intro, mỗi ảnh, outro và crossfade.
Giữ thời gian crossfade ngắn hơn từng cảnh; với bộ cảnh hiện tại nên giữ
`transitionSeconds` dưới nửa thời lượng cảnh ngắn nhất để các chuyển cảnh không chồng nhau.
Thời lượng tổng = tổng thời lượng cảnh − tổng thời gian crossfade.

Màu sắc và hoa/lấp lánh nằm trong `src/components/SceneFrame.tsx`.
Font dùng Arial/Georgia hoặc font dự phòng trên máy; muốn đồng nhất tuyệt đối giữa máy
cần bổ sung font local ở giai đoạn hoàn thiện.

## Xuất MP4 ở giai đoạn sau

Lệnh đã sẵn sàng, **chưa chạy trong giai đoạn 1**:

```bash
npm run render
```

Kết quả: `out/oppo-bac-ninh-20-10.mp4`, H.264, yuv420p, 2560 × 1440.
Nếu cần dùng Chromium đã cài:

```bash
npm run render -- --browser-executable=/usr/bin/chromium
```

## Cấu trúc mã nguồn

```text
src/
  index.ts                 # Entry Remotion
  Root.tsx                 # Composition chính + từng cảnh
  OppoVideo.tsx            # Timeline và nhạc tùy chọn
  timing.ts                # Thời lượng và phép tính overlap
  data/content.ts          # Nội dung, danh sách ảnh, nhạc
  components/SceneFrame.tsx # Khung, hoa, lấp lánh, animation chữ
  scenes/                  # Intro, Slideshow, PhotoScene, Outro
public/
  photos/                  # Ba SVG mẫu; thay bằng ảnh nhân sự
  music/                   # Chỗ đặt nhạc nền
```

`package-lock.json` khóa dependencies để cài lại bằng `npm ci`.
`node_modules/`, `build/`, `out/`, file môi trường và thư mục kiểm tra `work/` được bỏ qua trong Git.
