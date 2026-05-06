function onebit(sequence: String) {
    let count: number = 0
    for (const char of sequence) {
        if (char == "N") (
            count += 1
        )
    }

    return count/sequence.length * 100
}

function twobit(sequence: String) {
    let count: number = 0
    let state: string = "N"

    for (const char of sequence) {
        if (char == state) {
            count += 1
        } else {
            state = char
        }
    }
    return count/sequence.length * 100
} 

function fourbit(sequence: String) {
    let count: number = 0
    // we use two strings to represent a the multiple states
    // NN = strongly NT, NT = weakly NT, TN = weakly taken, TT = taken

    let state: string = "N"
    let prev: string = "N"  

    for (const char of sequence) {
        if (char == state) {
            count += 1
        } else {
            if (char == "T") {
                if (state == "N") {
                    if (prev == "N") {
                        prev = "T"
                    } else {
                        state = "T"
                        prev = "N"
                    }
                }
            } else {
                if (prev == "T") {
                    state = "T"
                    prev = "N"
                } else {
                    state = "N"
                    prev = "T"
                }
            }
        }
    }
    return count/sequence.length * 100
}
console.log(onebit("NNNNN"))
console.log(onebit("NNTNN"))
