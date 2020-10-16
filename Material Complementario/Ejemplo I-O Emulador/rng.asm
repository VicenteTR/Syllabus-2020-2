DATA:
seed 16
res1 -3
res2 -6
CODE:
call setear_semilla
call generar_random
mov (res1),a
call reset
call setear_semilla
call generar_random
mov (res2),a

jmp end

generar_random:
    in 8 ; leo el estado
    cmp a,2
    jne no_puedo_calcularo
    mov a,1
    out 11
    esperando_numero:
        in 8
        cmp a,2
        jne esperando_numero
    in 9
    mov b,0
    jmp final_gen_random
    no_puedo_calcularo:
        ; los códigos de error se pasan en el reg b
        cmp a,0
        jne si_tengo_semilla_al_menos_un_poco
        mov b,-1
        jmp final_gen_random
        si_tengo_semilla_al_menos_un_poco:
            cmp a,1
            jne si_tengo_semilla
            mov b,-2
            jmp final_gen_random

        si_tengo_semilla:
            cmp a,3
            jne no_esta_ocupado
            mov b,-3
            jmp final_gen_random
        no_esta_ocupado:
            cmp a,4
            jne error_desconocido
            mov b,-4
            jmp final_gen_random
        error_desconocido:
            mov b,-5
    final_gen_random:
ret


setear_semilla:
    mov a,(seed)
    out 10
    esperando_semilla_escrita:
        in 8
        cmp a,2
        jne esperando_semilla_escrita
    mov a,0
    out 11

    esperando_setee_semilla:
        in 8
        cmp a,2
        jne esperando_setee_semilla
    mov b,0
ret

reset:
    mov a,2
    out 11
    esperando_se_resetee:
        in 8
        cmp a,0
        jne esperando_se_resetee
ret





end:
