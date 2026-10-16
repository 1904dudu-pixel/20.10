export type Photo = {
  /** Đường dẫn tương đối trong public/, không bắt đầu bằng dấu /. */
  src: string;
  name: string;
  caption: string;
  objectPosition?: string;
};

// Nội dung mẫu; thay tên, lời chúc và file ảnh tại đây.
export const content = {
  organization: 'OPPO BẮC NINH',
  occasion: 'CHÀO MỪNG NGÀY PHỤ NỮ VIỆT NAM',
  introTitle: 'Tôn vinh nét đẹp',
  introAccent: 'của riêng bạn',
  introMessage: 'Gửi những người phụ nữ tuyệt vời\ncủa đại gia đình OPPO Bắc Ninh.',
  outroTitle: 'Luôn rạng rỡ.',
  outroAccent: 'Luôn là chính mình.',
  outroMessage: 'Chúc bạn một ngày 20/10 thật hạnh phúc,\nngập tràn yêu thương và những điều tốt đẹp.',
  signature: 'Với tất cả sự trân trọng • OPPO Bắc Ninh',
};

// Thêm hoặc bớt phần tử: thời lượng video tự cập nhật.
export const photos: Photo[] = [
  {
    src: 'photos/sample-01.svg',
    name: 'Rạng rỡ mỗi ngày',
    caption: 'Chúc bạn luôn tự tin, xinh đẹp\nvà tỏa sáng theo cách riêng.',
    objectPosition: 'center',
  },
  {
    src: 'photos/sample-02.svg',
    name: 'Cùng nhau tỏa sáng',
    caption: 'Cảm ơn những nỗ lực, nụ cười\nvà sự tận tâm bạn mang đến mỗi ngày.',
    objectPosition: 'center',
  },
  {
    src: 'photos/sample-03.svg',
    name: 'Yêu thương trọn vẹn',
    caption: 'Mong mọi hành trình phía trước\nđều có niềm vui và hạnh phúc đồng hành.',
    objectPosition: 'center',
  },
];

// Để null khi chưa có nhạc. Ví dụ sau này: 'music/nhac-nen.mp3'.
export const music: {src: string | null; volume: number} = {
  src: null,
  volume: 0.35,
};
