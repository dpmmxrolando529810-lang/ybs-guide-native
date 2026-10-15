# YBS Guide — Native Android

[နောက်ဆုံး APK](https://github.com/dpmmxrolando529810-lang/ybs-guide-native/releases/latest) · [ဖုန်းမှ Update ထုတ်ရန်](https://github.com/dpmmxrolando529810-lang/ybs-guide-native/actions/workflows/release.yml)

1.1.0 တွင် Light/Dark/System Theme၊ မြန်မာ/English၊ ကတ်သီးသန့်စာမျက်နှာ၊ bus logo အသစ်၊ Offline မြေပုံနှင့် အတည်ပြုချက်ဖြင့် တည်နေရာမျှဝေခြင်းတို့ ပါဝင်သည်။ App ထဲ ရှာဖွေခြင်း၊ ခရီးစဉ်တွက်ခြင်း၊ ရန်ကုန်အခြေခံမြေပုံ၊ GPS နှင့် ပါပြီးသားမှတ်တိုင်အသံကို အင်တာနက်မလိုဘဲ သုံးနိုင်သည်။ အသေးစိတ်မြေပုံကို ကြိုဒေါင်းရမည်။ ကတ်နံပါတ်ဖြင့် အွန်လိုင်းစစ်ခြင်း၊ တည်နေရာမျှဝေခြင်းနှင့် App update တွင် အင်တာနက်လိုသည်။

မူရင်း Source ကို [source-v1.1.4](https://github.com/dpmmxrolando529810-lang/ybs-guide-native/releases/tag/source-v1.1.4) ရှိ **YBS-Guide-Source-v1.1.4.zip** မှ ယူပါ။ GitHub ၏ အလိုအလျောက် Source code archive နှင့် မတူပါ။ ZIP ထဲတွင် ဖိုင်တစ်ခုချင်း၏ SHA-256 စာရင်းပါသည်။ Stable APK ကို Android တွင် install စမ်းသပ်ပြီးမှ ထုတ်သည်။

နောက်ဗားရှင်းထုတ်ရန် ဖုန်း Browser မှ **Actions → Publish YBS Android update → Run workflow** ကိုဖွင့်ပါ။ မသုံးရသေးသော Version name နှင့် ပြောင်းလဲချက်ကို ဖြည့်ပြီး Run workflow နှိပ်ပါ။ 1.1.0/code20 ထွက်ပြီးနောက် Version code ကို အလွတ်ထားလျှင် အလိုအလျောက်တိုးပေးမည်။ မူလ signing configuration ကို encrypted Actions secrets တွင် ချိတ်ပြီးဖြစ်သည်။ ကုဒ်ပြောင်းလျှင် Source ZIP အသစ်ကို prerelease တင်ပြီး tag/filename အသစ်ကို ရွေးပါ။ Private signing ဖိုင်များကို public asset မတင်ပါနှင့်။

အသုံးပြုသူက **ဆက်တင် → App update → Update တင်မည်** ကို နှိပ်နိုင်သည်။ App က ပါပြီးသား HTTPS feed ကိုစစ်၊ APK ဒေါင်း၊ စစ်ဆေးပြီး Android installer ဖွင့်ပေးမည်။ Android က ခွင့်ပြုချက်/Install အတည်ပြုချက် တောင်းနိုင်သည်။

တည်နေရာမျှဝေသူက အချိန်ရွေး၍ စတင်ပြီး ကြည့်သူ၏ request ကို အတည်ပြုပေးရသည်။ ဖုန်းနှစ်လုံးမှ ၆ လုံးအတည်ပြုနံပါတ်ကို တိုက်စစ်ပါ။ မျှဝေနေကြောင်း မြင်ရပြီး ချက်ချင်းရပ်နိုင်သည်။ App နောက်ခံရောက်လျှင် မျှဝေမှုရပ်နားသည်။ ဖုန်းနှစ်လုံးလုံး အင်တာနက်လိုသည်။ အခမဲ့ Render ဝန်ဆောင်မှုက အိပ်နိုင်/ပြန်စနိုင်ပြီး session များ အမြဲမသိမ်းပါ။ တစ်ပြိုင်နက် အကန့်အသတ်မရှိ သုံးနိုင်ကြောင်း အာမခံမထားပါ။

မူလ route records ၁၄၂၊ directions ၂၇၇၊ မှတ်တိုင်အုပ်စု ၁,၆၃၁၊ ရင်းမြစ်ပါ ခန့်မှန်း GPS ၁,၄၁၄ နှင့် GPS မသိသေးသော ၂၁၇ ကို ထိန်းသိမ်းထားသည်။ ၂၀၂၆ တရားဝင်ဒေတာ အပြည့်အစုံကို အတည်ပြုမရသေးပါ။ မြို့နယ်/လမ်းဘက်မတူသော အမည်တူမှတ်တိုင်များကို မဖျက်ပါ။ မူရင်းအသံမှာ primary မှတ်တိုင် ၁,၀၉၅ ခုနှင့် ချိတ်ထားသည်။ ကျန်နေရာ/English အတွက် ဖုန်းတွင် Offline TTS voice ရှိရန်လိုပြီး မရှိလျှင် beep/notification သုံးသည်။

Android 35 emulator ပေါ်တွင် APK install၊ synthetic GPS၊ မြေပုံအစစ်ဒေါင်းခြင်း၊ Airplane Mode ဖြင့် App ပြန်ဖွင့်ခြင်းနှင့် sharer/viewer သီးခြားအခွင့်အရေးတို့ကို စစ်ထားသည်။ Redmi Note 13 Pro 5G China၊ Xiaomi Civi 3 China နှင့် ကတ်အစစ်ကို တိုက်ရိုက်မစမ်းထားပါ။ App ကို နိုင်ငံအမျိုးမျိုးမှ Android အသုံးပြုသူများ သုံးနိုင်သော်လည်း YBS လမ်းကြောင်းဒေတာသည် ရန်ကုန်အတွက် ဖြစ်သည်။
