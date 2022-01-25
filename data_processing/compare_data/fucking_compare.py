#!/user/bin/env python
# -*-coding:utf-8 -*-
# @CreateTime : 2021/10/29 16:42
# @Author :     xujiahui
# @Project :    robust_python
# @File :       fucking_compare.py
# @Version :    V0.0.1
# @Desc :       ?


from basic_compare import *
from data_processing.compare_data import (
    csv_path_teacher_titles_dlmu,
    csv_path_teacher_titles_std,
    csv_path_teacher_titles_local_unmapped,
    csv_path_teacher_titles_local_mapped,
    csv_path_classroom_types_dlmu,
    csv_path_classroom_types_std,
    csv_path_classroom_types_local_unmapped,
    csv_path_classroom_types_local_mapped,
)


def dump_csv(
    dlmu_path: str, std_path: str, csv_path_mapped: str, csv_path_unmapped: str
):
    list_dlmu_dim, list_std_dim = fill_dim_list(dlmu_path, std_path)
    dict_std_dim = {dim_tuple[1]: dim_tuple[0] for dim_tuple in list_std_dim}
    dlmu_list_mapped, dlmu_list_unmapped = compare_data(list_dlmu_dim, dict_std_dim)
    if dlmu_list_mapped:
        print("-" * 100)
        print("dlmu_list_mapped:")
        print(len(dlmu_list_mapped))
        write_csv(dlmu_list_mapped, csv_path_mapped)
    if dlmu_list_unmapped:
        print("-" * 100)
        print("dlmu_list_unmapped:")
        print(len(dlmu_list_unmapped))
        write_csv(dlmu_list_unmapped, csv_path_unmapped)


if __name__ == "__main__":

    # 教师职称
    # dump_csv(
    #     dlmu_path=csv_path_teacher_titles_dlmu,
    #     std_path=csv_path_teacher_titles_std,
    #     csv_path_mapped=csv_path_teacher_titles_local_mapped,
    #     csv_path_unmapped=csv_path_teacher_titles_local_unmapped,
    # )

    # 教室类型
    dump_csv(
        dlmu_path=csv_path_classroom_types_dlmu,
        std_path=csv_path_classroom_types_std,
        csv_path_mapped=csv_path_classroom_types_local_mapped,
        csv_path_unmapped=csv_path_classroom_types_local_unmapped,
    )
