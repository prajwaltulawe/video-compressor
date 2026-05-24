CODECS = {

    # H.264
    "h264": {
        "cpu": "libx264",
        "nvidia": "h264_nvenc",
        "intel": "h264_qsv",
        "amd": "h264_amf",
        "mac": "h264_videotoolbox"
    },

    # H.265 / HEVC
    "hevc": {
        "cpu": "libx265",
        "nvidia": "hevc_nvenc",
        "intel": "hevc_qsv",
        "amd": "hevc_amf",
        "mac": "hevc_videotoolbox"
    },

    # VP9
    "vp9": {
        "cpu": "libvpx-vp9"
    },

    # AV1
    "av1": {
        "cpu": "libsvtav1",
        "nvidia": "av1_nvenc",
        "intel": "av1_qsv"
    },

    # MPEG-4 Part 2
    "mpeg4": {
        "cpu": "mpeg4"
    },

    # Xvid
    "xvid": {
        "cpu": "libxvid"
    },

    # Motion JPEG
    "mjpeg": {
        "cpu": "mjpeg"
    },

    # ProRes
    "prores": {
        "cpu": "prores_ks"
    },

    # DNxHD
    "dnxhd": {
        "cpu": "dnxhd"
    },

    # Theora
    "theora": {
        "cpu": "libtheora"
    },

    # Huffyuv (lossless)
    "huffyuv": {
        "cpu": "huffyuv"
    },

    # FFV1 (archival lossless)
    "ffv1": {
        "cpu": "ffv1"
    },

    # CineForm
    "cineform": {
        "cpu": "cfhd"
    }
}