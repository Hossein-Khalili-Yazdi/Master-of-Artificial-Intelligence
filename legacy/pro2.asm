
include io.h

stacksg segment stack
db 512 dup(?)
stacksg ends

datasg segment
	mainArr dw 202 dup(0)
	str1 db '1.daryaft kod kala va rooz va mizane froush',10,13,'2.daryaft kod kala va rooz va namaesh froush',10,13,'3.namayesh hameye etelaat',10,13,'4.namayesh porfroushtarin rooz',10,13,'5.namayesh porfroushtarin kala',10,13,'6.exit',10,13,10,13,'Please Choose your Number:',0
	str21 db 10,13,'maghadir khaste shode ra vared konid',10,13,0
	str2 db 10,13,'kod kala:',0
	str3 db 10,13,'rooz froosh:',0
	str31 db 10,13,'mizan froosh:',0
	strKhateBad db 10,13,0
	kodkala dw ?
	kodrooz dw ?
	roozfroosh dw ?
	mizanfroosh dw ?
	str4 db 10,13,'porfroushtarin rooz:',0
	str5 db 10,13,'porfroushtarin kala',0
	porroz dw ?
	porkala dw ?
	vorudi dw ?
	offsetMainArr dw ?
	addInArr dw 0
	chap db ?
	strKalayeBadi db 10,13,'kalaye badi 1 ra vared konid',10,13,'bazgash b menu 0 ra vared konid:',10,13,0
	strMeghdarFroosh db 10,13,'meghdar fruosh:',0
	strcama db ', ',0
	counter2 dw 0
	sum dw 0
	max dw 0
	counter dw 0
	shomarandeh dw 0
	strMax db 10,13,'Por forush tarin rooz:',0
	dwpointer db 2
	maxAdd dw 0
	m1 dw ?
	m2 dw ?
	strDonoghte db ':',0
	maxkala dw ?
	strPorForousTarinKala db 10,13,'Por forush tarin kala:',0
	
	val db 10 dup(?)

datasg ends
codesg segment
	main proc far
		assume cs:codesg,ds:datasg,ss:stacksg
		mov ax, seg datasg
		mov ds, ax
		
		lea bx, mainArr ;addresse mainArr ra dar be dast miarim
		mov offsetMainArr, bx ;addresse mainArr ra dar motaghyere offsetMainArr zakhire mikonim
		menu:
		output str1
		inputs val , 6
		atoi val
		mov vorudi, ax
		cmp vorudi, 1
		je t1
		jmp g1
		t1:jmp case1
		case1:
			mov addInArr , 0
			;kod kala
			call kalayab
			;rooz froosh
			call roozyab
			;mizan froosh
			call sabtefroosh
			;bazgasht b menu
			output strKalayeBadi
			inputs val,6
			atoi val
			cmp ax , 0
			je menu
			cmp ax , 1
			je case1
			g1:
		cmp vorudi, 2
		je t2
		jmp g2
		t2:jmp case2
		case2:
		    mov addInArr , 0
			call kalayab
			call roozyab
			mov bx , offsetMainArr
			add bx , addInArr
			itoa chap , [bx]
			output strKhateBad
			output strMeghdarFroosh
			output chap
			output strKhateBad
			output strKhateBad
			jmp menu
			g2:
		cmp vorudi, 3
		je t3
		jmp g3
		t3:jmp case3
		case3:
			mov addInArr , 0
			mov cx , 200
			mov bx , offsetMainArr
			mov ax , 0
			myFor1:
				
				inc ax
				itoa counter , ax
				output counter
				output strDonoghte
				
				add bx , 2
				itoa chap , [bx]
				
				output chap
				output strcama
			loop myFor1
			output strKhateBad
			jmp menu
			g3:
		cmp vorudi, 4
		je t4
		jmp g4
		t4:jmp case4
		case4:
			mov ax , 0
			mov counter2 , ax
			mov shomarandeh , 18
			forRooz:
			    mov bx , offsetMainArr
				add bx , counter2
				mov ax , [bx]
				add sum , ax
				inc counter2
				inc counter2
				mov ax , shomarandeh
				cmp counter2 , ax
				je rozbadi
				jmp forRooz
				rozbadi:
					mov ax, sum
					cmp max , ax
					jl bozorgtar
					cmp shomarandeh , 398
					jge exit3
					inc counter2
					inc counter2
					add shomarandeh , 20
					mov sum , 0
					jmp forRooz
				bozorgtar:
					mov ax , sum
					mov max , ax
					mov ax , counter2
					mov maxAdd , ax
					inc counter2
					inc counter2
					add shomarandeh , 20
					cmp shomarandeh , 398
					jge exit3
					mov sum , 0
					jmp forRooz
				exit3:
				output strMax
				mov dx , 0
				mov ax , maxAdd
				mov bx , 20
				div bx
				itoa chap , ax
				output chap
				output strKhateBad
				output strKhateBad
				jmp menu
			g4:
		cmp vorudi, 5
		je t5
		jmp g5
		t5:jmp case5
		case5:
			mov bx , offsetMainArr
			myFor2:
				mov ax , [bx]
				mov m1 , ax
				add bx , 2
				mov ax , [bx]
				mov m2 , ax
				mov ax , m2
				cmp m1 , ax
				jg maxNevis
				mov ax , m2
				mov max , ax
				add bx , 2
				mov maxkala , bx
				cmp bx , 400
				je myExit
				jmp myFor2
			maxNevis:
				mov ax , m1
				mov max , ax
				sub bx , 2
				mov maxkala , bx
				add bx , 2
				cmp bx , 400
				je myExit
			jmp myFor2
		myExit:
				mov dx , 0
				mov ax , maxkala
				mov bx , 2
				div bx
				mov bx , 20
				div bx
				;mov ax , 20
				;sub ax , dx
				output strPorForousTarinKala
				itoa chap , dx
				output chap
				output strKhateBad
				output strKhateBad
			jmp menu
			g5:
		cmp vorudi, 6
		je t6
		jmp g6
		t6:jmp case6
		case6:
			mov ah , 00
			mov al , 03
			int 10h
			jmp exitFinal
			g6:
	exitFinal:
		mov ah,4ch
		mov al,0
		int 21h
	main endp
	kalayab proc near
		output str21
		output str2
		inputs val,6
		atoi val
		mul dwpointer
		add addInArr , ax
	ret
	kalayab endp
	roozyab proc near
			output str3
			inputs val,6
			atoi val
			mov bx , 10
			mul bx
			mul dwpointer
			add addInArr , ax
	ret 
	roozyab endp
	sabtefroosh proc near
			output str31
			inputs val,6
			atoi val
			mov mizanfroosh , ax
			mov bx , offsetMainArr
			add bx , addInArr
			mov [bx] , ax
			itoa mizanfroosh , [bx]
			;output mizanfroosh
	ret
	sabtefroosh endp
codesg ends
end main
