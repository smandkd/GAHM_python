#%%
import re

# 원본 파일과 새로운 파일 경로 설정
input_file = 'bwp282018.dat'
output_file = 'modified_bwp282018.dat'

# 파일 열기
with open(input_file, 'r') as in_fh, open(output_file, 'w') as out_fh:
    for line in in_fh:
        # 기압 값을 찾기 위한 정규 표현식 (네 자리 숫자)
        modified_line = re.sub(r'(\b\d{4}\b)', lambda x: str(int(x.group(0)) + 4), line)
        out_fh.write(modified_line)

print(f"Modified file saved as '{output_file}'")
# %%
