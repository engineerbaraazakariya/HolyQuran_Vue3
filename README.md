To use it from WSL, start by installing WSL with: `wsl --install -d Ubuntu --location d:\wsl`
then add chromium, x11, code and xdg-utils with these steps:
`sudo snap install --classic code`
`sudo snap install chromium`
`sudo snap install x11-utils-snap --edge`
`sudo apt install xdg-utils`

Used also some env aliases for faster dev like these:
`alias cdInstallApk='cd android/app/build/outputs/apk/debug/ && adb install -r -d *.apk && cd ../../../../../../'`
`alias mkrn='ionic build && npx cap sync android && ionic capacitor copy android && cd android && ./gradlew assembleDebug && cd ..; cdInstallApk && sleep 3 && adb shell am start -n com.acrasoftware.HolyQuran/.MainActivity'`
`alias adbconnect='sudo adb connect 192.168.1.100:40213'`
`alias npmi='npm i'`
`alias cdQuran='cd ~/HolyQuran_Vue3'`
`alias srcbsh='source ~/.bashrc'`
`alias getaabion='ionic build && npx cap sync android && cd android && ./gradlew bundleRelease && cp app/build/outputs/bundle/release/app-release.aab ../app-release.aab'`
