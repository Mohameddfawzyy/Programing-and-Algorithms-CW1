# Enigma Encoder

# ----------------- Enigma Settings -----------------
rotors = ("1", "2", "3","4","5")
reflector = "UKW-B"
ringSettings = "ABCDE"
ringPositions = "DEFXY"
plugboard = "AT BS DE FM IR KN LZ OW PV XY"

# ---------------------------------------------------

def caesarShift(str, amount):
    output = ""

    for i in range(0, len(str)):
        c = str[i]
        code = ord(c)
        if ((code >= 65) and (code <= 90)):
            c = chr(((code - 65 + amount) % 26) + 65)
        output = output + c

    return output


def encode(plaintext):
    global rotors, reflector, ringSettings, ringPositions, plugboard
    # Enigma Rotors and reflectors
    rotor1 = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
    rotor1Notch = "Q"
    rotor2 = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
    rotor2Notch = "E"
    rotor3 = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
    rotor3Notch = "V"
    rotor4 = "ESOVPZJAYQUIRHXLNFTGKDCMWB"
    rotor4Notch = "J"
    rotor5 = "VZBRGITYUPSDNHLXAWMJQOFECK"
    rotor5Notch = "Z"

    rotorDict = {"1": rotor1, "2": rotor2, "3": rotor3, "4": rotor4, "5": rotor5}
    rotorNotchDict = {"1": rotor1Notch, "2": rotor2Notch, "3": rotor3Notch, "4": rotor4Notch, "5": rotor5Notch}

    reflector1 = {"A": "Y", "Y": "A", "B": "R", "R": "B", "C": "U", "U": "C", "D": "H", "H": "D", "E": "Q", "Q": "E",
                  "F": "S", "S": "F", "G": "L", "L": "G", "I": "P", "P": "I", "J": "X", "X": "J", "K": "N", "N": "K",
                  "M": "O", "O": "M", "T": "Z", "Z": "T", "V": "W", "W": "V"}
    reflector2 = {"A": "F", "F": "A", "B": "V", "V": "B", "C": "P", "P": "C", "D": "J", "J": "D", "E": "I", "I": "E",
                  "G": "O", "O": "G", "H": "Y", "Y": "H", "K": "R", "R": "K", "L": "Z", "Z": "L", "M": "X", "X": "M",
                  "N": "W", "W": "N", "Q": "T", "T": "Q", "S": "U", "U": "S"}

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    rotorANotch = False
    rotorBNotch = False
    rotorCNotch = False
    rotorDNotch = False
    rotorENotch = False

    if reflector == "UKW-B":
        reflectorDict = reflector1
    else:
        reflectorDict = reflector2

    # A = outerLeft,  B = leftMid,  C=Mid ,D=rightMid     ,E=outerRight
    rotorA = rotorDict[rotors[0]]
    rotorB = rotorDict[rotors[1]]
    rotorC = rotorDict[rotors[2]]
    rotorD = rotorDict[rotors[3]]
    rotorE = rotorDict[rotors[4]]

    rotorANotch = rotorNotchDict[rotors[0]]
    rotorBNotch = rotorNotchDict[rotors[1]]
    rotorCNotch = rotorNotchDict[rotors[2]]
    rotorDNotch = rotorNotchDict[rotors[3]]
    rotorENotch = rotorNotchDict[rotors[4]]

    rotorALetter = ringPositions[0]
    rotorBLetter = ringPositions[1]
    rotorCLetter = ringPositions[2]
    rotorDLetter = ringPositions[3]
    rotorELetter = ringPositions[4]

    rotorASetting = ringSettings[0]
    offsetASetting = alphabet.index(rotorASetting)
    rotorBSetting = ringSettings[1]
    offsetBSetting = alphabet.index(rotorBSetting)
    rotorCSetting = ringSettings[2]
    offsetCSetting = alphabet.index(rotorCSetting)
    rotorDSetting = ringSettings[3]
    offsetDSetting = alphabet.index(rotorDSetting)
    rotorESetting = ringSettings[4]
    offsetESetting = alphabet.index(rotorESetting)

    rotorA = caesarShift(rotorA, offsetASetting)
    rotorB = caesarShift(rotorB, offsetBSetting)
    rotorC = caesarShift(rotorC, offsetCSetting)
    rotorD = caesarShift(rotorD, offsetDSetting)
    rotorE = caesarShift(rotorE, offsetESetting)

    if offsetASetting > 0:
        rotorA = rotorA[26 - offsetASetting:] + rotorA[0:26 - offsetASetting]
    if offsetBSetting > 0:
        rotorB = rotorB[26 - offsetBSetting:] + rotorB[0:26 - offsetBSetting]
    if offsetCSetting > 0:
        rotorC = rotorC[26 - offsetCSetting:] + rotorC[0:26 - offsetCSetting]
    if offsetDSetting > 0:
        rotorD = rotorD[26 - offsetDSetting:] + rotorD[0:26 - offsetDSetting]
    if offsetESetting > 0:
        rotorE = rotorE[26 - offsetESetting:] + rotorE[0:26 - offsetESetting]

    ciphertext = ""

    # Converplugboard settings into a dictionary
    plugboardConnections = plugboard.upper().split(" ")
    plugboardDict = {}
    for pair in plugboardConnections:
        if len(pair) == 2:
            plugboardDict[pair[0]] = pair[1]
            plugboardDict[pair[1]] = pair[0]

    plaintext = plaintext.upper()
    for letter in plaintext:
        encryptedLetter = letter
#========================================
        if letter in alphabet:
            # Rotate Rotors - This happens as soon as a key is pressed, before encrypting the letter!
            rotorTrigger = False
            # Third rotor rotates by 1 for every key being pressed
            if rotorELetter == rotorENotch:
                rotorTrigger = True
            rotorELetter = alphabet[(alphabet.index(rotorELetter) + 1) % 26]
            # Check if rotorB needs to rotate
            if rotorTrigger:
                rotorTrigger = False
                if rotorDLetter == rotorDNotch:
                    rotorTrigger = True
                rotorDLetter = alphabet[(alphabet.index(rotorDLetter) + 1) % 26]

                if rotorTrigger:
                    rotorTrigger = False
                    if rotorCLetter == rotorCNotch:
                        rotorTrigger = True
                    rotorCLetter = alphabet[(alphabet.index(rotorCLetter) + 1) % 26]

                    if rotorTrigger:
                        rotorTrigger = False
                        if rotorBLetter == rotorBNotch:
                            rotorTrigger = True
                        rotorBLetter = alphabet[(alphabet.index(rotorBLetter) + 1) % 26]

                        # Check if rotorA needs to rotate
                        if (rotorTrigger):
                            rotorTrigger = False
                            rotorALetter = alphabet[(alphabet.index(rotorALetter) + 1) % 26]

            else:
                # Check for double step sequence!
                if rotorDLetter == rotorDNotch:
                    rotorDLetter = alphabet[(alphabet.index(rotorDLetter) + 1) % 26]
                    rotorCLetter = alphabet[(alphabet.index(rotorCLetter) + 1) % 26]
                    rotorBLetter = alphabet[(alphabet.index(rotorBLetter) + 1) % 26]
                    rotorALetter = alphabet[(alphabet.index(rotorALetter) + 1) % 26]

#======================================================================
            # Implement plugboard encryption!
            if letter in plugboardDict.keys():
                if plugboardDict[letter] != "":
                    encryptedLetter = plugboardDict[letter]

            # Rotors & Reflector Encryption
            offsetA = alphabet.index(rotorALetter)
            offsetB = alphabet.index(rotorBLetter)
            offsetC = alphabet.index(rotorCLetter)
            offsetD = alphabet.index(rotorDLetter)
            offsetE = alphabet.index(rotorELetter)

            # Wheel 5 Encryption
            pos = alphabet.index(encryptedLetter)
            let = rotorE[(pos + offsetE) % 26]
            pos = alphabet.index(let)
            encryptedLetter = alphabet[(pos - offsetE + 26) % 26]

            # Wheel 4 Encryption
            pos = alphabet.index(encryptedLetter)
            let = rotorD[(pos + offsetD) % 26]
            pos = alphabet.index(let)
            encryptedLetter = alphabet[(pos - offsetD + 26) % 26]

            # Wheel 3 Encryption
            pos = alphabet.index(encryptedLetter)
            let = rotorC[(pos + offsetC) % 26]
            pos = alphabet.index(let)
            encryptedLetter = alphabet[(pos - offsetC + 26) % 26]

            # Wheel 2 Encryption
            pos = alphabet.index(encryptedLetter)
            let = rotorB[(pos + offsetB) % 26]
            pos = alphabet.index(let)
            encryptedLetter = alphabet[(pos - offsetB + 26) % 26]

            # Wheel 1 Encryption
            pos = alphabet.index(encryptedLetter)
            let = rotorA[(pos + offsetA) % 26]
            pos = alphabet.index(let)
            encryptedLetter = alphabet[(pos - offsetA + 26) % 26]

            # Reflector encryption!
            if encryptedLetter in reflectorDict.keys():
                if reflectorDict[encryptedLetter] != "":
                    encryptedLetter = reflectorDict[encryptedLetter]

            # Back through the rotors
            # Wheel 1 Encryption
            pos = alphabet.index(encryptedLetter)
            let = alphabet[(pos + offsetA) % 26]
            pos = rotorA.index(let)
            encryptedLetter = alphabet[(pos - offsetA + 26) % 26]

            # Wheel 2 Encryption
            pos = alphabet.index(encryptedLetter)
            let = alphabet[(pos + offsetB) % 26]
            pos = rotorB.index(let)
            encryptedLetter = alphabet[(pos - offsetB + 26) % 26]

            # Wheel 3 Encryption
            pos = alphabet.index(encryptedLetter)
            let = alphabet[(pos + offsetC) % 26]
            pos = rotorC.index(let)
            encryptedLetter = alphabet[(pos - offsetC + 26) % 26]

            # Wheel 4 Encryption
            pos = alphabet.index(encryptedLetter)
            let = alphabet[(pos + offsetD) % 26]
            pos = rotorD.index(let)
            encryptedLetter = alphabet[(pos - offsetD + 26) % 26]

            # Wheel 5 Encryption
            pos = alphabet.index(encryptedLetter)
            let = alphabet[(pos + offsetE) % 26]
            pos = rotorE.index(let)
            encryptedLetter = alphabet[(pos - offsetE + 26) % 26]


            # Implement plugboard encryption!
            if encryptedLetter in plugboardDict.keys():
                if plugboardDict[encryptedLetter] != "":
                    encryptedLetter = plugboardDict[encryptedLetter]

        ciphertext = ciphertext + encryptedLetter

    return ciphertext


# Main Program Starts Here
print("#### Enigma Encoder #####")
print("")
plaintext = input("Enter text to encode or decode:\n")
ciphertext = encode(plaintext)


print("\nEncoded text: \n " + ciphertext)
