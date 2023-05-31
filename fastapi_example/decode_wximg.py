# 参考自： https://zhuanlan.zhihu.com/p/130314175
import os
import glob

# 图片字节头信息，
# [0][1]为jpg头信息，
# [2][3]为png头信息，
# [4][5]为gif头信息
pic_heads = [0xff, 0xd8, 0x89, 0x50, 0x47, 0x49]
pic_exts = ["jpg", "png", "gif"]


def get_code(file_path):
    """
    自动判断文件类型，并获取dat文件解密码
    :param file_path: dat文件路径
    :return: 如果文件为jpg/png/gif格式，则返回解密码，否则返回0
    """
    dat_file = open(file_path, "rb")
    dat_read = dat_file.read(2)
    head_index = 0
    while head_index < len(pic_heads):
        # 使用第一个头信息字节来计算加密码
        # 第二个字节来验证解密码是否正确
        code = dat_read[0] ^ pic_heads[head_index]
        idf_code = dat_read[1] ^ code
        head_index = head_index + 1
        if idf_code == pic_heads[head_index]:
            dat_file.close()
            return pic_exts[head_index // 2], code
        head_index = head_index + 1

    print("not jpg, png, gif")
    return "", 0

def search_dat(file_path):
    return glob.glob(file_path[:-1] + '*')[0]

def decode_dat(file_path):
    """
    解密文件，并生成图片
    :param file_path: dat文件路径
    :return: None或图片绝对路径
    """
    file_path = search_dat(file_path)
    if not os.path.isfile(file_path):
        return None
    if not os.path.isdir(".\\img"):
        os.mkdir("img")
    pic_ext, decode_code = get_code(file_path)
    if decode_code == 0:
        return None
    dat_file = open(file_path, "rb")
    pic_path = ".\\img\\" + file_path.split("\\")[-1] + "." + pic_ext
    pic_path = os.path.abspath(pic_path)
    if os.path.isfile(pic_path):
        return pic_path
    pic_write = open(pic_path, "wb")
    for dat_data in dat_file:
        for dat_byte in dat_data:
            pic_data = dat_byte ^ decode_code
            pic_write.write(bytes([pic_data]))
    dat_file.close()
    pic_write.close()
    return pic_path
