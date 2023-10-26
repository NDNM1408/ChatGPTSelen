import os
from dotenv import load_dotenv

if __name__ == "__main__":
    question = "Việc trích lập dự phòng nghiệp vụ của doanh nghiệp kinh doanh bảo hiểm phải bảo đảm những yêu cầu nào?"
    passage = "Khoản 2 Điều 97 Luật Kinh doanh bảo hiểm 2022 quy định về các yêu cầu với việc trích lập dự phòng nghiệp vụ như sau: Dự phòng nghiệp vụ 1. Dự phòng nghiệp vụ là khoản tiền mà doanh nghiệp bảo hiểm, doanh nghiệp tái bảo hiểm, chi nhánh nước ngoài tại Việt Nam phải trích lập nhằm mục đích thanh toán cho những trách nhiệm bảo hiểm có thể phát sinh từ các hợp đồng bảo hiểm đã giao kết. 2. Việc trích lập dự phòng nghiệp vụ phải bảo đảm các yêu cầu sau đây: a) Trích lập riêng cho từng nghiệp vụ bảo hiểm; b) Tương ứng với phần trách nhiệm đã cam kết theo thỏa thuận trong hợp đồng bảo hiểm; c) Tách biệt giữa các hợp đồng bảo hiểm của đối tượng bảo hiểm trong và ngoài phạm vi lãnh thổ Việt Nam, kể cả trong cùng một nghiệp vụ bảo hiểm, sản phẩm bảo hiểm, trừ trường hợp pháp luật có quy định khác; d) Luôn có tài sản tương ứng với dự phòng nghiệp vụ đã trích lập, đồng thời tách biệt tài sản tương ứng với dự phòng quy định tại điểm c khoản này; đ) Sử dụng Chuyên gia tính toán để tính toán, trích lập dự phòng nghiệp vụ; e) Thường xuyên rà soát, đánh giá việc trích lập dự phòng nghiệp vụ; kịp thời có các biện pháp nhằm bảo đảm trích lập đầy đủ dự phòng để chi trả cho các trách nhiệm của doanh nghiệp bảo hiểm, doanh nghiệp tái bảo hiểm, chi nhánh nước ngoài tại Việt Nam. ... "
    prompt = f"Trả lời bằng Tiếng Việt.     Ngữ cảnh:    {passage}       Câu hỏi: {question}"
    prompt_preprocess = prompt.replace("\n", " "*4)
    print(prompt_preprocess)
