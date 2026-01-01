Knight's Tour Visualizer with PyQt5
Chess Knight
تطبيق رسومي تفاعلي لحل مشكلة جولة الفارس (Knight's Tour) على رقعة الشطرنج باستخدام Python و PyQt5
هذا البرنامج يتيح لك تجربة ومقارنة خوارزميات بحث مختلفة لحل مشكلة Knight's Tour، مع أنيميشن جميل لحركة الفارس على الرقعة، وعرض عدد العقد الموسعة، والتحكم في السرعة.
clipartmax.comWhite Chess Knight Icon - Free Transparent PNG Clipart Images Download
المميزات الرئيسية

دعم رقعتين: 5x5 و 8x8
اختيار موقع البداية بالنقر على المربع
خوارزميات متعددة:
BFS (Breadth-First Search)
DFS (Depth-First Search)
Greedy (مع heuristic Warnsdorff)
A*
Warnsdorff's Rule (الأكثر كفاءة عملياً)

أنيميشن حركة الفارس مع صورة knight.png
شريط تحكم في السرعة (0-100%)
عرض عدد العقد الموسعة أثناء البحث
زر Stop لإيقاف الحل في أي وقت
تغيير لون الخلفية عند إيجاد حل كامل (أخضر) أو جزئي (برتقالي)

stackoverflow.comstackoverflow.com

أمثلة على مسارات Knight's Tour
runestone.academychess-teacher.commedium.com


المتطلبات

Python 3.x
PyQt5

طريقة التشغيل

تأكد من تثبيت PyQt5:textpip install PyQt5
ضع صورة knight.png في نفس مجلد الكود (يمكنك استخدام أي صورة فارس شطرنج بحجم مناسب).
شغل البرنامج:textpython knights_tour_pyqt.py

كيفية الاستخدام

اختر حجم الرقعة (5x5 أو 8x8)
انقر على مربع لتحديد موقع البداية
اختر الخوارزمية المطلوبة
اضغط Go لبدء الحل مع الأنيميشن
استخدم الشريط الجانبي للتحكم في السرعة
اضغط Stop إذا أردت إيقاف العملية

ملاحظة: خوارزمية Warnsdorff و Greedy غالباً ما تجدان حلولاً كاملة بسرعة كبيرة على 8x8، بينما BFS/DFS قد تكون بطيئة جداً بسبب الحجم الهائل لفضاء البحث.
ترخيص
MIT License - يمكنك استخدامه وتعديله بحرية.

استمتع بمشاهدة الفارس وهو يجول الرقعة! ♞✨
إذا أعجبك المشروع، لا تنسَ إعطاء ⭐ على GitHub!