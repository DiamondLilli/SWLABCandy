#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>

int main() {
    int ret=fork();
    int fd = open("out.txt", O_CREAT | O_RDWR | O_TRUNC, 0644);

    if (fd < 0) {
        perror("open");
        exit(1);
    }

    write(fd, "B", 1);

    if (ret == 0) {
        // Child
        execlp("./writer", "./writer", NULL);
        perror("execlp");
        exit(1);
    } else {
        // Parent
        // wait(NULL);
        
        write(fd, "A", 1);
        close(fd);
    }
    return 0;
}
