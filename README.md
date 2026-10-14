# YBS Guide — Native Android

လက်ရှိ အသုံးပြုရန် **v1.0.12 / code13** ဖြစ်သည်။ Android8 နှင့်အထက် အသုံးပြုနိုင်ပြီး target Android16 ဖြစ်သည်။ MapLibre Native ပါဝင်သည်။

[APK ဒေါင်းလုဒ်](https://github.com/dpmmxrolando529810-lang/ybs-guide-native/releases/download/v1.0.12/YBS-Guide-v1.0.12.apk) · [Latest release](https://github.com/dpmmxrolando529810-lang/ybs-guide-native/releases/latest) · [Verified Source v1.0.12](https://github.com/dpmmxrolando529810-lang/ybs-guide-native/releases/tag/source-v1.0.12)

## App Update

မူလ App မဖျက်ဘဲ v1.0.12 APK ကို ပထမတစ်ကြိမ် Update အဖြစ် install လုပ်ပါ။ v1.0.11 တွင် default feed မပါသေးသောကြောင့် ပထမဆုံး configured APK ကို ကိုယ်တိုင် install လုပ်ရသည်။

နောက်ဗားရှင်းများအတွက် **Application Update → Update တင်မည်** ကို တစ်ချက်နှိပ်ပါ။ App က ဗားရှင်းစစ်၊ ဒေါင်းလုဒ်၊ လက်မှတ်/ဖိုင်စစ်ပြီး Install ဆက်လုပ်သည်။ URL ဖြည့်ရန် မလိုပါ။ Android က source permission သို့မဟုတ် Install အတည်ပြုချက် တောင်းနိုင်သည်။

လက်ရှိနောက်ဆုံးဗားရှင်းက v1.0.12 ဖြစ်သေးလျှင် Update အသစ်မရှိကြောင်း ပြမည်။ APK ၏ SHA-256:

`a9b0159be997388d2cdb7236f0fd8ed5ab995f3bd9c865e7c7cf4e4ba2bc693a`

## ဖုန်းမှ နောက်ဗားရှင်း ထုတ်ရန်

GitHub Native Build စစ်ဆေးမှု အောင်မြင်သည်။ Source ZIP၊ Publisher/archive tests၊ Android SDK၊ APK signature နှင့် 16KB alignment စစ်ပြီးဖြစ်သည်။

[GitHub Build စစ်ဆေးမှု](https://github.com/dpmmxrolando529810-lang/ybs-guide-native/actions/runs/38626760428) သည် **ယာယီ QA signer** ဖြင့် တည်ဆောက်သည်။ Production signing secrets ကို မသုံးပါ။ ဤစစ်ဆေးမှုက App release အသစ် မထုတ်ပါ။

မူလ App signing key ကို encrypted Actions secret အဖြစ် ချိတ်ပြီးဖြစ်သည်။ **မူလ App signing password ကို `YBS_RELEASE_PASSWORD` အဖြစ် သိမ်းရန် owner ခွင့်ပြုချက် ကျန်နေသည်။** ထိုအဆင့်ပြီးမှ မူလလက်မှတ်တူ GitHub cloud release ထုတ်နိုင်မည်။ Account login password ကို မလိုပါ။

Signing password ချိတ်ပြီးနောက် ဖုန်း Browser ဖြင့်:

1. **Actions → Publish YBS Android update → Run workflow** ကို ဖွင့်ပါ။
2. နောက် release အတွက် **Version name = 1.0.13** ဖြည့်ပါ။ နောက်ထပ် release များတွင် အမည်အသစ် သုံးပါ။ ထုတ်ပြီးသား tag ကို ပြန်မသုံးပါနှင့်။
3. **Version code** ကို အလွတ်ထားပါ။ လက်ရှိ code13 မှ နောက် code14 ကို အလိုအလျောက်တိုးမည်။
4. **Source tag = source-v1.0.12**, **Source asset = YBS-Guide-Source-v1.0.12.zip** ကို default အတိုင်း ထားပါ။
5. ပြင်ဆင်ချက်ကို Release notes တွင် ရေးပြီး **Run workflow** နှိပ်ပါ။

မပြည့်စုံသော signing configuration ကို workflow အစတွင် ရပ်ပေးသည်။ Build ပြီးလျှင် package၊ မူလ signing certificate၊ version/code၊ size/hash၊ built-in feed နှင့် uploaded Draft assets ကို စစ်မှ Latest အဖြစ် ထုတ်သည်။ Public feed နှင့် APK ကို login မပါဘဲ ပြန်ဒေါင်းလုဒ်စစ်သည်။

Source code အသစ်ရှိလျှင် Source ZIP အသစ်ကို သီးခြား **Source prerelease** အဖြစ်တင်ပြီး tag/filename ကို ပြောင်းရွေးပါ။ Source prerelease ကို Latest အဖြစ် မထားပါနှင့်။ Source ZIP အဟောင်းကို workflow က feature အသစ် အလိုအလျောက် ထည့်မပေးပါ။

PC၊ VPS သို့မဟုတ် Termux မလိုပါ။ ဤ configuration သည် standard `ubuntu-24.04` runner ကို သုံးသည်။ Paid runner သို့မဟုတ် Actions artifact upload မသတ်မှတ်ထားပါ။

## ဒေတာနှင့် စစ်ဆေးမှု

| အချက် | အရေအတွက် |
| --- | ---: |
| မူလ published route records | 142 |
| ရင်းမြစ်တွင် ဖော်ပြထားသော direction lists | 277 |
| Name + road + township အလိုက် primary stop groups | 1,631 |
| ရင်းမြစ်ပါ ခန့်မှန်း GPS ရှိသော groups | 1,414 |
| GPS မသိသေးသော groups | 217 |

Source/data consistency စစ်ဆေးချက် **62,195** နှင့် application extraction/import စစ်ဆေးချက် **83,177** အောင်သည်။ Application input13ခုအနက်8ခုမှ ဒေတာရရှိထားသည်။ ကျန်5ခုတွင် reusable ဒေတာ မရရှိသေးပါ။

**၂၀၂၆ တရားဝင်ဒေတာ အပြည့်အစုံကို အတည်မပြုနိုင်သေးပါ။** လက်ရှိ စစ်ဆေးချက်များသည် retained source consistency ကို စစ်ခြင်းဖြစ်ပြီး ကွင်းဆင်း GPS အတည်ပြုခြင်း မဟုတ်ပါ။

ပြန်စစ်ထားသော ရင်းမြစ်များ: [JICA GTFS](https://jicayangonbusta.wordpress.com/up-to-date-information-for-gtfs/) သည် 2020-09-29 update၊ 2021-06-30 end date ကို ဖော်ပြသည်။ [YBPC operator website](https://www.yangonbuspubliccompany.com/) တွင် ရက်စွဲမပါသော line/endpoints စာရင်း ရှိသော်လည်း current stop/GPS master အပြည့်အစုံ မရရှိပါ။

Physical Redmi Android16၊ live NFC/card၊ အသံအသိပေးနှင့် real GPS တို့ကို ဤ cloud compilation မှ အတည်ပြုထားခြင်း မရှိပါ။ v1.0.11 ၏ Android8/12 updater integration နှင့် v1.0.10 map rendering စမ်းသပ်ချက်များသည် သမိုင်းမှတ်တမ်းများ ဖြစ်သည်။
