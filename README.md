# YBS Guide — ဖုန်းမှ Update ထုတ်ဝေရန်

လက်ရှိ public APK သည် **1.0.14 / code15** ဖြစ်သည်။ မူလ YBS signing certificate ဖြင့် GitHub ပေါ်တွင် build၊ metadata ထုတ်၊ upload စစ်ပြီး Latest အဖြစ် ထုတ်ဝေမှု အောင်မြင်ပြီးဖြစ်သည်။

- [လက်ရှိ APK release](https://github.com/dpmmxrolando529810-lang/ybs-guide-native/releases/tag/v1.0.14)
- [အောင်မြင်သော production build](https://github.com/dpmmxrolando529810-lang/ybs-guide-native/actions/runs/38633710908)
- [ပြင်ပြီးသား Source 1.0.14](https://github.com/dpmmxrolando529810-lang/ybs-guide-native/releases/tag/source-v1.0.14)

## App ထဲမှ Update လုပ်ရန်

v1.0.12 တင်ပြီးသူသည် **Application Update → Update တင်မည်** ကို တစ်ချက်နှိပ်ပါ။ App က version စစ်၊ ဒေါင်းလုဒ်၊ ဖိုင်နှင့်လက်မှတ်စစ်ပြီး Install ဆက်လုပ်သည်။ URL ဖြည့်ရန် မလိုပါ။ Android က source permission သို့မဟုတ် Install အတည်ပြုချက်တောင်းလျှင် အတည်ပြုပါ။

v1.0.11 သို့မဟုတ် ပိုဟောင်းသော app တွင် Update ရင်းမြစ်မပါသေးပါ။ အထက်ပါ release မှ APK ကို ပထမတစ်ကြိမ် မူလ app မဖျက်ဘဲ Update အဖြစ် တင်ပါ။ နောက်မှ app ထဲက Update ခလုတ်ကို သုံးနိုင်သည်။ လက်ရှိ 1.0.14 တင်ပြီးလျှင် နောက်ဗားရှင်း မထုတ်သေးချိန် update မတွေ့ခြင်းသည် ပုံမှန်ဖြစ်သည်။

## ဖုန်း Browser မှ နောက် Version ထုတ်ရန်

မူလ signing key နှင့် signing password နှစ်ခုလုံး encrypted GitHub Actions secrets တွင် ချိတ်ထားပြီးဖြစ်သည်။ Public Source ZIP နှင့် APK ထဲတွင် private signing material မပါပါ။ Account login password ကို app update အတွက် မလိုပါ။

1. Repository → **Actions → Publish YBS Android update → Run workflow** သို့ ဝင်ပါ။
2. Branch ကို **main** ထားပါ။ နောက် Version name ကို **1.0.15** ဖြည့်ပါ။ နောက်ပိုင်းတွင် မသုံးရသေးသော အမည်အသစ် သုံးပါ။
3. Version code ကို အလွတ်ထားပါ။ လက်ရှိ code15 ထက်မြင့်သော **code16** ကို အလိုအလျောက်ရွေးမည်။
4. Source tag **source-v1.0.14** နှင့် Source asset **YBS-Guide-Source-v1.0.14.zip** ကို default အတိုင်းထားနိုင်သည်။ Source အသစ်ပြင်ထားလျှင် checksum ပါသော Source ZIP အသစ်ကို သီးခြား prerelease အဖြစ် တင်ပြီး သက်ဆိုင်ရာ tag/filename ရွေးပါ။
5. Release notes ဖြည့်ပြီး **Run workflow** ကို နှိပ်ပါ။ အောင်မြင်သည်အထိ `.github/workflows/` ဖိုင်များကို မပြင်ပါနှင့်။ GitHub က ယခင် workflow commit ကို release target အဖြစ် သုံးခြင်းကို ကန့်သတ်နိုင်သည်။
6. Workflow တွင် **Success** ပြပြီး release စာမျက်နှာ၌ APK၊ update.json နှင့် SHA256SUMS.txt ပေါ်ကြောင်း ကြည့်ပါ။

Publisher သည် Source ZIP digest/ဖိုင်တစ်ခုချင်း checksum၊ မူလ package/certificate၊ ပိုမြင့်သော version code၊ APK size/SHA-256 နှင့် built-in update feed တို့ကို စစ်သည်။ Draft asset များမှန်မှ Latest အဖြစ် ထုတ်ပြီး public JSON နှင့် APK အပြည့်အစုံကို Login မပါဘဲ ပြန်ဒေါင်းလုဒ်စစ်သည်။

SDK executable permission error နှင့် unpublished draft ကို ID ဖြင့် စစ်ဆေးထုတ်ဝေခြင်းတို့ကို 1.0.14 Source တွင် ပြင်ထားသည်။ Source 1.0.12 သည် ထိုပြင်ဆင်မှုမပါသော သမိုင်း snapshot ဖြစ်သည်။ ယခု repository main workflow များကို သုံးပါ။

## အတည်ပြုထားသည့် အတိုင်းအတာ

Production GitHub build၊ မူလ APK certificate၊ 16KB ZIP alignment၊ public feed နှင့် APK size/hash စစ်ဆေးမှုများ အောင်သည်။ ဒေတာ asset 1860 ခုနှင့် MapLibre Native library 4 ခုသည် v1.0.12 နှင့် byte တူသည်။ App engine နှင့် မြေပုံဒေတာကို ယခု release တွင် ဆက်လက်အသုံးပြုထားသည်။

မူလ route records 142၊ directions 277၊ stop groups 1631၊ ရင်းမြစ်ပါ ခန့်မှန်း GPS 1414 နှင့် မသိသေးသော GPS 217 ကို ထိန်းသိမ်းထားသည်။ 2026 တရားဝင်ဒေတာ အပြည့်အစုံ အတည်ပြုမှုနှင့် ဖုန်းအစစ် Redmi Android16/GPS/NFC/card/အသံ စမ်းသပ်မှု မပြီးသေးပါ။ ယခင် emulator စမ်းသပ်ချက်များမှာ သမိုင်းမှတ်တမ်းများ ဖြစ်သည်။
