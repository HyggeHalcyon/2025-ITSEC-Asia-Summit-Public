#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <signal.h>
#include <unistd.h>
#include <string.h>

#define MAX 4

typedef struct {
    unsigned long seconds;
    unsigned long snooze;
} _alarm;

typedef struct {
    char title[0x8];
} title;

unsigned long _[4] = {0x0};
unsigned long used[MAX] = {0x0};
title titles[MAX] = {0x0};
_alarm* alarms[MAX] = {0x0};

#define RED     "\033[1;31m"
#define GREEN   "\033[1;32m"
#define YELLOW  "\033[1;33m"
#define BLUE    "\033[1;34m"
#define MAGENTA "\033[1;35m"
#define CYAN    "\033[1;36m"
#define RESET   "\033[0m"

void alarm_handler(int sig) {
    printf(RED "\n\n💥💥💥 REALITY STRIKES! 💥💥💥\n" RESET);
    printf(RED "You woke up... your waifu is gone...\n\n" RESET);
}

long get_idx() {
    char buf[8] = {0x0};
    long n = read(0, buf, sizeof(buf));
    if (strlen(buf) != 0) {
        long idx = atoi(buf);
        if (idx < 0 || idx >= MAX) exit(1);
        return idx;
    }
    return n;
}

void setup_alarm(long seconds) {
    printf(YELLOW "[⏰] You'll halu for %ld seconds... Enjoy your dream~\n" RESET, seconds);

    struct sigaction sa;
    sigemptyset(&sa.sa_mask);
    sa.sa_handler = alarm_handler;
    sa.sa_flags = 0;
    sigaction(SIGALRM, &sa, NULL);

    alarm(seconds);
}

void create() {
    printf(MAGENTA "\n🌸 [Create New Halu Session] 🌸\n" RESET);
    printf(" >> Pilih slot halu (0-%d): ", MAX - 1);
    unsigned long idx = get_idx();

    alarms[idx] = malloc(0x1e0);

    printf(" >> Durasi nge-halu (detik): ");
    unsigned long seconds = 0;
    scanf("%llu%*c", &seconds);
    alarms[idx]->seconds = seconds;

    printf(" >> Snooze tambahan (detik): ");
    unsigned long snooze = 0;
    scanf("%llu%*c", &snooze);
    alarms[idx]->snooze = snooze;

    printf(" >> Nama waifu impianmu: ");
    read(0, &titles[idx], 0x8);

    used[idx] = 0;
    printf(GREEN "[✓] Halusinasi dengan %s selama %lu detik telah disiapkan\n" RESET, titles[idx].title, seconds);
}

void use() {
    printf(MAGENTA "\n✨ [Masuki Dunia Halu] ✨\n" RESET);
    printf(" >> Slot halu yang ingin dipakai: ");
    unsigned long idx = get_idx();

    if (used[idx] || alarms[idx] == NULL) {
        printf(RED "[!] alamak, halunya dah dipake ato kosong 😵\n" RESET);
        return;
    }

    printf(GREEN "🌈 Kamu memejamkan mata... %s memanggilmu dari dunia mimpi...\n" RESET, titles[idx].title);
    setup_alarm(alarms[idx]->seconds);
    used[idx] = 1;
    free(alarms[idx]);
    printf(RED "[!] halu[%ld] berakhir...\n" RESET, idx);
}

void edit() {
    printf(MAGENTA "\n📝 [Ubah Halu Lama] 📝\n" RESET);
    printf(" >> Slot halu: ");
    unsigned long idx = get_idx();

    if (used[idx] || alarms[idx] == NULL) {
        printf(RED "[!] alamak, tak bole la... halu sudah dipake ato kosong\n" RESET);
        return;
    }

    unsigned long seconds = 0;
    printf(" >> Durasi baru: ");
    scanf("%llu%*c", &seconds);
    alarms[idx]->seconds = seconds;

    printf(" >> Snooze baru: ");
    unsigned long snooze = 0;
    scanf("%llu%*c", &snooze);
    alarms[idx]->snooze = snooze;

    printf(" >> Ganti waifu ke: ");
    read(0, &titles[idx], 0x8);

    printf(GREEN "[✓] Halusinasi slot[%ld] sekarang dengan %s selama %lu detik\n" RESET, idx, titles[idx].title, seconds);
}

void check() {
    printf(CYAN "\n🔍 [Cek Halusinasi] 🔍\n" RESET);
    printf(" >> Slot halu: ");
    unsigned long idx = get_idx();
    printf(YELLOW "[*] Memeriksa slot[%lu]...\n" RESET, idx);

    if (alarms[idx] == NULL) {
        printf(RED "[!] Slot kosong... hayoloh ngimpi kosong 😴\n" RESET);
        return;
    }

    printf(BLUE "🌸 Bersama %s selama %lu detik\n" RESET, &titles[idx], alarms[idx]->seconds);
}

unsigned int menu() {
    puts(YELLOW "\n==============================");
    puts("      🌙 HALU SIMULATOR 🌙");
    puts("==============================" RESET);
    puts(" 1. Buat sesi nge-halu");
    puts(" 2. Masuki dunia halu");
    puts(" 3. Edit sesi halu");
    puts(" 4. Cek jadwal halu");
    puts(" 5. Bangun dari mimpi 😭");
    printf(CYAN "\n>> Pilihanmu: " RESET);

    unsigned int choice = 0;
    scanf("%u", &choice);
    getchar();
    return choice;
}

void main(int argc, char *argv[]) {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    printf(MAGENTA "\nSelamat datang di dunia halu, di mana waifumu menunggumu...\n" RESET);
    while (1) {
        unsigned int choice = menu();
        switch (choice) {
            case 1:
                create();
                break;
            case 2:
                use();
                break;
            case 3:
                edit();
                break;
            case 4:
                check();
                break;
            case 5:
                printf(RED "\nKamu memilih untuk bangun... sampai jumpa, waifu...\n" RESET);
                exit(0);
            default:
                puts(RED "[!] Pilihan tidak valid, fokus napa!\n" RESET);
                break;
        }
    }
}
