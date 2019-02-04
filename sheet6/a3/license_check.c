#include <stdio.h>

void validate(char *l){
    if(strlen(l) != 29) printf("erro\n");
    int i14 = 0;
    do {
        if(i14 >= 29) break;
        if((i14 != 5) && (i14 != 11) && (i14 != 17) && (i14 != 23)){
            if((l[i14] <= 47) || (l[i14] > 57)){
                if(l[i14] > 64){
                    if(l[i14] > 90)
                        return printf("erro1\n");
                } else return printf("erro2\n");
            }
        } else {
            if(l[i14] != 45) return printf("erro3\n");
        }
        i14++;
    } while(1);
    if(l[4] ^ l[0] ^ l[1] ^ l[2] ^ l[3] != 65) printf("erro4\n");
    if(l[6] ^ l[7] ^ l[8] != l[10]) printf("erro5\n");
    if(l[12] & l[13] & l[14] & l[15] != l[16]) printf("erro6\n");
    if((int)((l[20] | l[18] | l[22]) & 0xf) != (int)(l[19] ^ l[21])) printf("erro7 %d %d %d %d\n", l[20], l[18], l[22], l[19]^l[21]);
    if(((int)(l[24]) != (int)(l[25]-1))) printf("erro8\n");
    if((int)(l[26]) != (int)(l[27]+1)) printf("erro9\n");
    if((l[28] != 88)) printf("erro10\n");
}


int main() {   // 111  
    char l[30] = "AAAAA-AAAAA-AAAAA-AMALA-ABBAX";// len must be 29
    //int ebp_120 = l[4];
    int i;
    validate(l);
    return 0;
}

//; Variables:
//        ;    var_14: int32_t, -20
//        ;    var_20: int64_t, -32
//        ;    var_28: int64_t, -40
//       ;    var_114: int8_t, -276  23 28
//        ;    var_115: int8_t, -277 22 27
//        ;    var_116: int8_t, -278 21 26
//        ;    var_117: int8_t, -279 20 25
//        ;    var_118: int8_t, -280 19 24
//        ;    var_11A: int8_t, -282 18 22
//        ;    var_11B: int8_t, -283 17 21
//        ;    var_11C: int8_t, -284 16 20
//        ;    var_11D: int8_t, -285 15 19
//        ;    var_11E: int8_t, -286 14 18
//        ;    var_120: int8_t, -288 13 16
//        ;    var_121: int8_t, -289 12 15
//        ;    var_122: int8_t, -290 11 14
//        ;    var_123: int8_t, -291 10 l[13]
//        ;    var_124: int8_t, -292 9 l[12]
//        ;    var_126: int8_t, -294 8 l[10]
//        ;    var_128: int8_t, -296 7 l[8]
//        ;    var_129: int8_t, -297 6 l[7]
//        ;    var_12A: int8_t, -298 5 l[6]
//                 12B:         -299 l[5]
//        ;    var_12C: int8_t, -300 l[4]
//        ;    var_12D: int8_t, -301 l[3]
//        ;    var_12E: int8_t, -302 l[2]
//        ;    var_12F: int8_t, -303 l[1]
//        ;    var_130: int8_t, -304 l[0]
//        ;    var_134: int32_t, -308
//        ;    var_140: int64_t, -320
