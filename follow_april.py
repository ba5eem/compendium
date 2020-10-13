import math
import threading
import olympe
from olympe.messages.ardrone3.Piloting import TakeOff, moveBy, Landing, moveTo, Circle, PCMD
from olympe.messages.ardrone3.PilotingState import moveToChanged, FlyingStateChanged, PositionChanged, AttitudeChanged
from olympe.messages.ardrone3.GPSSettingsState import GPSFixStateChanged
from olympe.messages.ardrone3.PilotingState import GpsLocationChanged
from olympe.enums.ardrone3.Piloting import MoveTo_Orientation_mode

route = [
  [ [ 21.368492831528414, -157.712818 ] ],
  [ [ 21.368447915764207, -157.71276976863433 ] ],
  [ [ 21.368403, -157.71272153726866 ] ],
  [ [ 21.368447915764207, -157.71286623136567 ] ],
  [ [ 21.368403, -157.71272153726866 ] ],
  [ [ 21.368358084235798, -157.712673305903 ] ],
  [ [ 21.368358084235798, -157.712962694097 ] ]
] ,
[
  [ [ 21.368582663056824, -157.712818 ] ],
  [ [ 21.368537747292617, -157.71276976860474 ] ],
  [ [ 21.36849283152841, -157.7127215372095 ] ],
  [ [ 21.368537747292617, -157.71286623139525 ] ],
  [ [ 21.36849283152841, -157.7127215372095 ] ],
  [ [ 21.368447915764207, -157.71267330581423 ] ],
  [ [ 21.368447915764207, -157.71296269418576 ] ]
] ,
[
  [ [ 21.368672494585237, -157.712818 ] ],
  [ [ 21.36862757882103, -157.71276976857516 ] ],
  [ [ 21.368582663056824, -157.71272153715032 ] ],
  [ [ 21.36862757882103, -157.71286623142484 ] ],
  [ [ 21.368582663056824, -157.71272153715032 ] ],
  [ [ 21.36853774729262, -157.71267330572547 ] ],
  [ [ 21.36853774729262, -157.71296269427452 ] ]
] ,
[
  [ [ 21.36876232611365, -157.712818 ] ],
  [ [ 21.368717410349443, -157.71276976854557 ] ],
  [ [ 21.368672494585237, -157.71272153709114 ] ],
  [ [ 21.368717410349443, -157.71286623145443 ] ],
  [ [ 21.368672494585237, -157.71272153709114 ] ],
  [ [ 21.368627578821034, -157.7126733056367 ] ],
  [ [ 21.368627578821034, -157.71296269436328 ] ]
] ,
[
  [ [ 21.36885215764206, -157.712818 ] ],
  [ [ 21.368807241877853, -157.71276976851598 ] ],
  [ [ 21.368762326113647, -157.71272153703197 ] ],
  [ [ 21.368807241877853, -157.712866231484 ] ],
  [ [ 21.368762326113647, -157.71272153703197 ] ],
  [ [ 21.368717410349443, -157.71267330554795 ] ],
  [ [ 21.368717410349443, -157.71296269445205 ] ]
] ,
[
  [ [ 21.368941989170473, -157.712818 ] ],
  [ [ 21.368897073406266, -157.7127697684864 ] ],
  [ [ 21.36885215764206, -157.7127215369728 ] ],
  [ [ 21.368897073406266, -157.7128662315136 ] ],
  [ [ 21.36885215764206, -157.7127215369728 ] ],
  [ [ 21.368807241877857, -157.7126733054592 ] ],
  [ [ 21.368807241877857, -157.7129626945408 ] ]
] ,
[
  [ [ 21.369031820698883, -157.712818 ] ],
  [ [ 21.368986904934676, -157.7127697684568 ] ],
  [ [ 21.36894198917047, -157.71272153691362 ] ],
  [ [ 21.368986904934676, -157.7128662315432 ] ],
  [ [ 21.36894198917047, -157.71272153691362 ] ],
  [ [ 21.368897073406266, -157.71267330537043 ] ],
  [ [ 21.368897073406266, -157.71296269462957 ] ]
] ,
[
  [ [ 21.369121652227296, -157.712818 ] ],
  [ [ 21.36907673646309, -157.71276976842722 ] ],
  [ [ 21.369031820698883, -157.71272153685445 ] ],
  [ [ 21.36907673646309, -157.71286623157278 ] ],
  [ [ 21.369031820698883, -157.71272153685445 ] ],
  [ [ 21.36898690493468, -157.71267330528167 ] ],
  [ [ 21.36898690493468, -157.71296269471833 ] ]
] ,
[
  [ [ 21.36921148375571, -157.712818 ] ],
  [ [ 21.369166567991503, -157.71276976839764 ] ],
  [ [ 21.369121652227296, -157.71272153679527 ] ],
  [ [ 21.369166567991503, -157.71286623160236 ] ],
  [ [ 21.369121652227296, -157.71272153679527 ] ],
  [ [ 21.369076736463093, -157.7126733051929 ] ],
  [ [ 21.369076736463093, -157.7129626948071 ] ]
] ,
[
  [ [ 21.36930131528412, -157.712818 ] ],
  [ [ 21.369256399519912, -157.71276976836805 ] ],
  [ [ 21.369211483755706, -157.7127215367361 ] ],
  [ [ 21.369256399519912, -157.71286623163195 ] ],
  [ [ 21.369211483755706, -157.7127215367361 ] ],
  [ [ 21.369166567991503, -157.71267330510412 ] ],
  [ [ 21.369166567991503, -157.71296269489588 ] ]
] ,
[
  [ [ 21.369391146812532, -157.712818 ] ],
  [ [ 21.369346231048326, -157.71276976833846 ] ],
  [ [ 21.36930131528412, -157.7127215366769 ] ],
  [ [ 21.369346231048326, -157.71286623166154 ] ],
  [ [ 21.36930131528412, -157.7127215366769 ] ],
  [ [ 21.369256399519916, -157.71267330501536 ] ],
  [ [ 21.369256399519916, -157.71296269498464 ] ]
] ,
[
  [ [ 21.369480978340945, -157.712818 ] ],
  [ [ 21.36943606257674, -157.71276976830887 ] ],
  [ [ 21.369391146812532, -157.71272153661772 ] ],
  [ [ 21.36943606257674, -157.71286623169112 ] ],
  [ [ 21.369391146812532, -157.71272153661772 ] ],
  [ [ 21.36934623104833, -157.7126733049266 ] ],
  [ [ 21.36934623104833, -157.7129626950734 ] ]
] ,
[
  [ [ 21.369570809869355, -157.712818 ] ],
  [ [ 21.36952589410515, -157.7127697682793 ] ],
  [ [ 21.369480978340942, -157.71272153655855 ] ],
  [ [ 21.36952589410515, -157.7128662317207 ] ],
  [ [ 21.369480978340942, -157.71272153655855 ] ],
  [ [ 21.36943606257674, -157.71267330483784 ] ],
  [ [ 21.36943606257674, -157.71296269516216 ] ]
] ,
[
  [ [ 21.36966064139777, -157.712818 ] ],
  [ [ 21.36961572563356, -157.7127697682497 ] ],
  [ [ 21.369570809869355, -157.71272153649937 ] ],
  [ [ 21.36961572563356, -157.7128662317503 ] ],
  [ [ 21.369570809869355, -157.71272153649937 ] ],
  [ [ 21.369525894105152, -157.71267330474907 ] ],
  [ [ 21.369525894105152, -157.71296269525092 ] ]
] ,
[
  [ [ 21.36975047292618, -157.712818 ] ],
  [ [ 21.369705557161975, -157.71276976822008 ] ],
  [ [ 21.36966064139777, -157.7127215364402 ] ],
  [ [ 21.369705557161975, -157.7128662317799 ] ],
  [ [ 21.36966064139777, -157.7127215364402 ] ],
  [ [ 21.369615725633565, -157.71267330466029 ] ],
  [ [ 21.369615725633565, -157.7129626953397 ] ]
] ,
[
  [ [ 21.36984030445459, -157.712818 ] ],
  [ [ 21.369795388690385, -157.7127697681905 ] ],
  [ [ 21.369750472926178, -157.71272153638103 ] ],
  [ [ 21.369795388690385, -157.7128662318095 ] ],
  [ [ 21.369750472926178, -157.71272153638103 ] ],
  [ [ 21.369705557161975, -157.71267330457152 ] ],
  [ [ 21.369705557161975, -157.71296269542847 ] ]
] ,
[
  [ [ 21.369930135983005, -157.712818 ] ],
  [ [ 21.369885220218798, -157.7127697681609 ] ],
  [ [ 21.36984030445459, -157.71272153632185 ] ],
  [ [ 21.369885220218798, -157.7128662318391 ] ],
  [ [ 21.36984030445459, -157.71272153632185 ] ],
  [ [ 21.369795388690388, -157.71267330448276 ] ],
  [ [ 21.369795388690388, -157.71296269551723 ] ]
] ,
[
  [ [ 21.370019967511414, -157.712818 ] ],
  [ [ 21.369975051747208, -157.71276976813132 ] ],
  [ [ 21.369930135983, -157.71272153626265 ] ],
  [ [ 21.369975051747208, -157.71286623186867 ] ],
  [ [ 21.369930135983, -157.71272153626265 ] ],
  [ [ 21.369885220218798, -157.712673304394 ] ],
  [ [ 21.369885220218798, -157.712962695606 ] ]
] ,
[
  [ [ 21.370109799039827, -157.712818 ] ],
  [ [ 21.37006488327562, -157.71276976810174 ] ],
  [ [ 21.370019967511414, -157.71272153620347 ] ],
  [ [ 21.37006488327562, -157.71286623189826 ] ],
  [ [ 21.370019967511414, -157.71272153620347 ] ],
  [ [ 21.36997505174721, -157.7126733043052 ] ],
  [ [ 21.36997505174721, -157.71296269569478 ] ]
] ,
[
  [ [ 21.37019963056824, -157.712818 ] ],
  [ [ 21.370154714804034, -157.71276976807215 ] ],
  [ [ 21.370109799039827, -157.7127215361443 ] ],
  [ [ 21.370154714804034, -157.71286623192785 ] ],
  [ [ 21.370109799039827, -157.7127215361443 ] ],
  [ [ 21.370064883275624, -157.71267330421645 ] ],
  [ [ 21.370064883275624, -157.71296269578355 ] ]
] ,
[
  [ [ 21.37019963056824, -157.7127215361443 ] ],
  [ [ 21.370154714804034, -157.71267330421645 ] ],
  [ [ 21.370109799039827, -157.7126250722886 ] ],
  [ [ 21.370154714804034, -157.71276976807215 ] ],
  [ [ 21.370109799039827, -157.7126250722886 ] ],
  [ [ 21.370064883275624, -157.71257684036075 ] ],
  [ [ 21.370064883275624, -157.71286623192785 ] ]
] ,
[
  [ [ 21.37019963056824, -157.7126250722886 ] ],
  [ [ 21.370154714804034, -157.71257684036075 ] ],
  [ [ 21.370109799039827, -157.7125286084329 ] ],
  [ [ 21.370154714804034, -157.71267330421645 ] ],
  [ [ 21.370109799039827, -157.7125286084329 ] ],
  [ [ 21.370064883275624, -157.71248037650506 ] ],
  [ [ 21.370064883275624, -157.71276976807215 ] ]
] ,
[
  [ [ 21.37019963056824, -157.7125286084329 ] ],
  [ [ 21.370154714804034, -157.71248037650506 ] ],
  [ [ 21.370109799039827, -157.7124321445772 ] ],
  [ [ 21.370154714804034, -157.71257684036075 ] ],
  [ [ 21.370109799039827, -157.7124321445772 ] ],
  [ [ 21.370064883275624, -157.71238391264936 ] ],
  [ [ 21.370064883275624, -157.71267330421645 ] ]
] ,
[
  [ [ 21.37019963056824, -157.7124321445772 ] ],
  [ [ 21.370154714804034, -157.71238391264936 ] ],
  [ [ 21.370109799039827, -157.7123356807215 ] ],
  [ [ 21.370154714804034, -157.71248037650506 ] ],
  [ [ 21.370109799039827, -157.7123356807215 ] ],
  [ [ 21.370064883275624, -157.71228744879366 ] ],
  [ [ 21.370064883275624, -157.71257684036075 ] ]
] ,
[
  [ [ 21.37019963056824, -157.7123356807215 ] ],
  [ [ 21.370154714804034, -157.71228744879366 ] ],
  [ [ 21.370109799039827, -157.7122392168658 ] ],
  [ [ 21.370154714804034, -157.71238391264936 ] ],
  [ [ 21.370109799039827, -157.7122392168658 ] ],
  [ [ 21.370064883275624, -157.71219098493796 ] ],
  [ [ 21.370064883275624, -157.71248037650506 ] ]
] ,
[
  [ [ 21.37019963056824, -157.7122392168658 ] ],
  [ [ 21.370154714804034, -157.71219098493796 ] ],
  [ [ 21.370109799039827, -157.7121427530101 ] ],
  [ [ 21.370154714804034, -157.71228744879366 ] ],
  [ [ 21.370109799039827, -157.7121427530101 ] ],
  [ [ 21.370064883275624, -157.71209452108226 ] ],
  [ [ 21.370064883275624, -157.71238391264936 ] ]
] ,
[
  [ [ 21.37019963056824, -157.7121427530101 ] ],
  [ [ 21.370154714804034, -157.71209452108226 ] ],
  [ [ 21.370109799039827, -157.71204628915442 ] ],
  [ [ 21.370154714804034, -157.71219098493796 ] ],
  [ [ 21.370109799039827, -157.71204628915442 ] ],
  [ [ 21.370064883275624, -157.71199805722657 ] ],
  [ [ 21.370064883275624, -157.71228744879366 ] ]
] ,
[
  [ [ 21.37019963056824, -157.71204628915442 ] ],
  [ [ 21.370154714804034, -157.71199805722657 ] ],
  [ [ 21.370109799039827, -157.71194982529872 ] ],
  [ [ 21.370154714804034, -157.71209452108226 ] ],
  [ [ 21.370109799039827, -157.71194982529872 ] ],
  [ [ 21.370064883275624, -157.71190159337087 ] ],
  [ [ 21.370064883275624, -157.71219098493796 ] ]
] ,
[
  [ [ 21.37019963056824, -157.71194982529872 ] ],
  [ [ 21.370154714804034, -157.71190159337087 ] ],
  [ [ 21.370109799039827, -157.71185336144302 ] ],
  [ [ 21.370154714804034, -157.71199805722657 ] ],
  [ [ 21.370109799039827, -157.71185336144302 ] ],
  [ [ 21.370064883275624, -157.71180512951517 ] ],
  [ [ 21.370064883275624, -157.71209452108226 ] ]
] ,
[
  [ [ 21.37019963056824, -157.71185336144302 ] ],
  [ [ 21.370154714804034, -157.71180512951517 ] ],
  [ [ 21.370109799039827, -157.71175689758732 ] ],
  [ [ 21.370154714804034, -157.71190159337087 ] ],
  [ [ 21.370109799039827, -157.71175689758732 ] ],
  [ [ 21.370064883275624, -157.71170866565947 ] ],
  [ [ 21.370064883275624, -157.71199805722657 ] ]
] ,
[
  [ [ 21.37019963056824, -157.7117568975873 ] ],
  [ [ 21.370154714804034, -157.71170866565944 ] ],
  [ [ 21.370109799039827, -157.7116604337316 ] ],
  [ [ 21.370154714804034, -157.71180512951514 ] ],
  [ [ 21.370109799039827, -157.7116604337316 ] ],
  [ [ 21.370064883275624, -157.71161220180375 ] ],
  [ [ 21.370064883275624, -157.71190159337084 ] ]
] ,
[
  [ [ 21.37019963056824, -157.7116604337316 ] ],
  [ [ 21.370154714804034, -157.71161220180375 ] ],
  [ [ 21.370109799039827, -157.7115639698759 ] ],
  [ [ 21.370154714804034, -157.71170866565944 ] ],
  [ [ 21.370109799039827, -157.7115639698759 ] ],
  [ [ 21.370064883275624, -157.71151573794805 ] ],
  [ [ 21.370064883275624, -157.71180512951514 ] ]
] ,
[
  [ [ 21.37019963056824, -157.7115639698759 ] ],
  [ [ 21.370154714804034, -157.71151573794805 ] ],
  [ [ 21.370109799039827, -157.7114675060202 ] ],
  [ [ 21.370154714804034, -157.71161220180375 ] ],
  [ [ 21.370109799039827, -157.7114675060202 ] ],
  [ [ 21.370064883275624, -157.71141927409235 ] ],
  [ [ 21.370064883275624, -157.71170866565944 ] ]
] ,
[
  [ [ 21.37019963056824, -157.7114675060202 ] ],
  [ [ 21.370154714804034, -157.71141927409235 ] ],
  [ [ 21.370109799039827, -157.7113710421645 ] ],
  [ [ 21.370154714804034, -157.71151573794805 ] ],
  [ [ 21.370109799039827, -157.7113710421645 ] ],
  [ [ 21.370064883275624, -157.71132281023665 ] ],
  [ [ 21.370064883275624, -157.71161220180375 ] ]
] ,
[
  [ [ 21.37019963056824, -157.7113710421645 ] ],
  [ [ 21.370154714804034, -157.71132281023665 ] ],
  [ [ 21.370109799039827, -157.7112745783088 ] ],
  [ [ 21.370154714804034, -157.71141927409235 ] ],
  [ [ 21.370109799039827, -157.7112745783088 ] ],
  [ [ 21.370064883275624, -157.71122634638095 ] ],
  [ [ 21.370064883275624, -157.71151573794805 ] ]
] ,
[
  [ [ 21.37019963056824, -157.7112745783088 ] ],
  [ [ 21.370154714804034, -157.71122634638095 ] ],
  [ [ 21.370109799039827, -157.7111781144531 ] ],
  [ [ 21.370154714804034, -157.71132281023665 ] ],
  [ [ 21.370109799039827, -157.7111781144531 ] ],
  [ [ 21.370064883275624, -157.71112988252526 ] ],
  [ [ 21.370064883275624, -157.71141927409235 ] ]
] ,
[
  [ [ 21.37019963056824, -157.7111781144531 ] ],
  [ [ 21.370154714804034, -157.71112988252526 ] ],
  [ [ 21.370109799039827, -157.7110816505974 ] ],
  [ [ 21.370154714804034, -157.71122634638095 ] ],
  [ [ 21.370109799039827, -157.7110816505974 ] ],
  [ [ 21.370064883275624, -157.71103341866956 ] ],
  [ [ 21.370064883275624, -157.71132281023665 ] ]
] ,
[
  [ [ 21.37019963056824, -157.7110816505974 ] ],
  [ [ 21.370154714804034, -157.71103341866956 ] ],
  [ [ 21.370109799039827, -157.7109851867417 ] ],
  [ [ 21.370154714804034, -157.71112988252526 ] ],
  [ [ 21.370109799039827, -157.7109851867417 ] ],
  [ [ 21.370064883275624, -157.71093695481386 ] ],
  [ [ 21.370064883275624, -157.71122634638095 ] ]
] ,
[
  [ [ 21.37019963056824, -157.7109851867417 ] ],
  [ [ 21.370154714804034, -157.71093695481386 ] ],
  [ [ 21.370109799039827, -157.710888722886 ] ],
  [ [ 21.370154714804034, -157.71103341866956 ] ],
  [ [ 21.370109799039827, -157.710888722886 ] ],
  [ [ 21.370064883275624, -157.71084049095816 ] ],
  [ [ 21.370064883275624, -157.71112988252526 ] ]
] ,
[
  [ [ 21.37019963056824, -157.710888722886 ] ],
  [ [ 21.370154714804034, -157.71084049095816 ] ],
  [ [ 21.370109799039827, -157.7107922590303 ] ],
  [ [ 21.370154714804034, -157.71093695481386 ] ],
  [ [ 21.370109799039827, -157.7107922590303 ] ],
  [ [ 21.370064883275624, -157.71074402710246 ] ],
  [ [ 21.370064883275624, -157.71103341866956 ] ]
] ,
[
  [ [ 21.370109799039827, -157.7107922590303 ] ],
  [ [ 21.37006488327562, -157.71074402713205 ] ],
  [ [ 21.370019967511414, -157.7106957952338 ] ],
  [ [ 21.37006488327562, -157.71084049092858 ] ],
  [ [ 21.370019967511414, -157.7106957952338 ] ],
  [ [ 21.36997505174721, -157.71064756333553 ] ],
  [ [ 21.36997505174721, -157.7109369547251 ] ]
] ,
[
  [ [ 21.370019967511418, -157.71069579517462 ] ],
  [ [ 21.36997505174721, -157.71064756330594 ] ],
  [ [ 21.369930135983005, -157.71059933143727 ] ],
  [ [ 21.36997505174721, -157.7107440270433 ] ],
  [ [ 21.369930135983005, -157.71059933143727 ] ],
  [ [ 21.3698852202188, -157.71055109956862 ] ],
  [ [ 21.3698852202188, -157.7108404907806 ] ]
] ,
[
  [ [ 21.369930135983005, -157.71059933131892 ] ],
  [ [ 21.369885220218798, -157.71055109947983 ] ],
  [ [ 21.36984030445459, -157.71050286764077 ] ],
  [ [ 21.369885220218798, -157.710647563158 ] ],
  [ [ 21.36984030445459, -157.71050286764077 ] ],
  [ [ 21.369795388690388, -157.71045463580168 ] ],
  [ [ 21.369795388690388, -157.71074402683615 ] ]
] ,
[
  [ [ 21.36984030445459, -157.71050286746322 ] ],
  [ [ 21.369795388690385, -157.71045463565372 ] ],
  [ [ 21.369750472926178, -157.71040640384425 ] ],
  [ [ 21.369795388690385, -157.71055109927272 ] ],
  [ [ 21.369750472926178, -157.71040640384425 ] ],
  [ [ 21.369705557161975, -157.71035817203474 ] ],
  [ [ 21.369705557161975, -157.7106475628917 ] ]
] ,
[
  [ [ 21.36975047292618, -157.71040640360752 ] ],
  [ [ 21.369705557161975, -157.7103581718276 ] ],
  [ [ 21.36966064139777, -157.71030994004772 ] ],
  [ [ 21.369705557161975, -157.71045463538744 ] ],
  [ [ 21.36966064139777, -157.71030994004772 ] ],
  [ [ 21.369615725633565, -157.7102617082678 ] ],
  [ [ 21.369615725633565, -157.71055109894724 ] ]
] ,
[
  [ [ 21.36966064139777, -157.71030993975182 ] ],
  [ [ 21.36961572563356, -157.71026170800152 ] ],
  [ [ 21.369570809869355, -157.7102134762512 ] ],
  [ [ 21.36961572563356, -157.71035817150212 ] ],
  [ [ 21.369570809869355, -157.7102134762512 ] ],
  [ [ 21.369525894105152, -157.7101652445009 ] ],
  [ [ 21.369525894105152, -157.71045463500275 ] ]
] ,
[
  [ [ 21.36957080986936, -157.71021347589613 ] ],
  [ [ 21.369525894105152, -157.7101652441754 ] ],
  [ [ 21.369480978340945, -157.71011701245467 ] ],
  [ [ 21.369525894105152, -157.71026170761684 ] ],
  [ [ 21.369480978340945, -157.71011701245467 ] ],
  [ [ 21.369436062576742, -157.71006878073396 ] ],
  [ [ 21.369436062576742, -157.7103581710583 ] ]
] ,
[
  [ [ 21.369480978340945, -157.71011701204043 ] ],
  [ [ 21.36943606257674, -157.7100687803493 ] ],
  [ [ 21.369391146812532, -157.71002054865815 ] ],
  [ [ 21.36943606257674, -157.71016524373155 ] ],
  [ [ 21.369391146812532, -157.71002054865815 ] ],
  [ [ 21.36934623104833, -157.70997231696703 ] ],
  [ [ 21.36934623104833, -157.71026170711383 ] ]
] ,
[
  [ [ 21.369391146812532, -157.71002054818473 ] ],
  [ [ 21.369346231048326, -157.7099723165232 ] ],
  [ [ 21.36930131528412, -157.70992408486163 ] ],
  [ [ 21.369346231048326, -157.71006877984627 ] ],
  [ [ 21.36930131528412, -157.70992408486163 ] ],
  [ [ 21.369256399519916, -157.7098758532001 ] ],
  [ [ 21.369256399519916, -157.71016524316937 ] ]
] ,
[
  [ [ 21.369301315284122, -157.70992408432903 ] ],
  [ [ 21.369256399519916, -157.70987585269708 ] ],
  [ [ 21.36921148375571, -157.70982762106513 ] ],
  [ [ 21.369256399519916, -157.70997231596098 ] ],
  [ [ 21.36921148375571, -157.70982762106513 ] ],
  [ [ 21.369166567991506, -157.70977938943315 ] ],
  [ [ 21.369166567991506, -157.7100687792249 ] ]
] ,
[
  [ [ 21.36921148375571, -157.7098276204733 ] ],
  [ [ 21.369166567991503, -157.70977938887094 ] ],
  [ [ 21.369121652227296, -157.70973115726858 ] ],
  [ [ 21.369166567991503, -157.70987585207567 ] ],
  [ [ 21.369121652227296, -157.70973115726858 ] ],
  [ [ 21.369076736463093, -157.70968292566621 ] ],
  [ [ 21.369076736463093, -157.7099723152804 ] ]
] ,
[
  [ [ 21.369121652227296, -157.7097311566176 ] ],
  [ [ 21.36907673646309, -157.70968292504483 ] ],
  [ [ 21.369031820698883, -157.70963469347205 ] ],
  [ [ 21.36907673646309, -157.70977938819038 ] ],
  [ [ 21.369031820698883, -157.70963469347205 ] ],
  [ [ 21.36898690493468, -157.70958646189928 ] ],
  [ [ 21.36898690493468, -157.70987585133594 ] ]
] ,
[
  [ [ 21.369031820698886, -157.7096346927619 ] ],
  [ [ 21.36898690493468, -157.70958646121872 ] ],
  [ [ 21.368941989170473, -157.70953822967553 ] ],
  [ [ 21.36898690493468, -157.7096829243051 ] ],
  [ [ 21.368941989170473, -157.70953822967553 ] ],
  [ [ 21.36889707340627, -157.70948999813234 ] ],
  [ [ 21.36889707340627, -157.70977938739148 ] ]
] ,
[
  [ [ 21.368941989170473, -157.7095382289062 ] ],
  [ [ 21.368897073406266, -157.7094899973926 ] ],
  [ [ 21.36885215764206, -157.709441765879 ] ],
  [ [ 21.368897073406266, -157.7095864604198 ] ],
  [ [ 21.36885215764206, -157.709441765879 ] ],
  [ [ 21.368807241877857, -157.7093935343654 ] ],
  [ [ 21.368807241877857, -157.70968292344702 ] ]
] ,
[
  [ [ 21.36885215764206, -157.7094417650505 ] ],
  [ [ 21.368807241877853, -157.7093935335665 ] ],
  [ [ 21.368762326113647, -157.70934530208248 ] ],
  [ [ 21.368807241877853, -157.70948999653453 ] ],
  [ [ 21.368762326113647, -157.70934530208248 ] ],
  [ [ 21.368717410349443, -157.70929707059847 ] ],
  [ [ 21.368717410349443, -157.70958645950256 ] ]
] ,
[
  [ [ 21.36876232611365, -157.70934530119482 ] ],
  [ [ 21.368717410349443, -157.7092970697404 ] ],
  [ [ 21.368672494585237, -157.70924883828596 ] ],
  [ [ 21.368717410349443, -157.70939353264924 ] ],
  [ [ 21.368672494585237, -157.70924883828596 ] ],
  [ [ 21.368627578821034, -157.70920060683153 ] ],
  [ [ 21.368627578821034, -157.7094899955581 ] ]
] ,
[
  [ [ 21.368672494585237, -157.70924883733912 ] ],
  [ [ 21.36862757882103, -157.70920060591428 ] ],
  [ [ 21.368582663056824, -157.70915237448943 ] ],
  [ [ 21.36862757882103, -157.70929706876396 ] ],
  [ [ 21.368582663056824, -157.70915237448943 ] ],
  [ [ 21.36853774729262, -157.7091041430646 ] ],
  [ [ 21.36853774729262, -157.70939353161364 ] ]
] ,
[
  [ [ 21.368582663056827, -157.70915237348342 ] ],
  [ [ 21.36853774729262, -157.70910414208817 ] ],
  [ [ 21.368492831528414, -157.7090559106929 ] ],
  [ [ 21.36853774729262, -157.70920060487867 ] ],
  [ [ 21.368492831528414, -157.7090559106929 ] ],
  [ [ 21.36844791576421, -157.70900767929766 ] ],
  [ [ 21.36844791576421, -157.70929706766918 ] ]
] ,
[
  [ [ 21.368492831528414, -157.70905590962772 ] ],
  [ [ 21.368447915764207, -157.70900767826205 ] ],
  [ [ 21.368403, -157.7089594468964 ] ],
  [ [ 21.368447915764207, -157.7091041409934 ] ],
  [ [ 21.368403, -157.7089594468964 ] ],
  [ [ 21.368358084235798, -157.70891121553072 ] ],
  [ [ 21.368358084235798, -157.70920060372472 ] ]
] ,
[
  [ [ 21.368403, -157.70895944577202 ] ],
  [ [ 21.368358084235794, -157.70891121443594 ] ],
  [ [ 21.368313168471587, -157.70886298309986 ] ],
  [ [ 21.368358084235794, -157.7090076771081 ] ],
  [ [ 21.368313168471587, -157.70886298309986 ] ],
  [ [ 21.368268252707384, -157.70881475176378 ] ],
  [ [ 21.368268252707384, -157.70910413978027 ] ]
] ,
[
  [ [ 21.368313168471587, -157.70905590844418 ] ],
  [ [ 21.36826825270738, -157.7090076771377 ] ],
  [ [ 21.368223336943174, -157.7089594458312 ] ],
  [ [ 21.36826825270738, -157.70910413975068 ] ],
  [ [ 21.368223336943174, -157.7089594458312 ] ],
  [ [ 21.36817842117897, -157.7089112145247 ] ],
  [ [ 21.36817842117897, -157.70920060236367 ] ]
] ,
[
  [ [ 21.368223336943178, -157.70915237111635 ] ],
  [ [ 21.36817842117897, -157.70910413983944 ] ],
  [ [ 21.368133505414765, -157.70905590856253 ] ],
  [ [ 21.36817842117897, -157.70920060239325 ] ],
  [ [ 21.368133505414765, -157.70905590856253 ] ],
  [ [ 21.36808858965056, -157.70900767728563 ] ],
  [ [ 21.36808858965056, -157.70929706494707 ] ]
] ,
[
  [ [ 21.368133505414765, -157.7092488337885 ] ],
  [ [ 21.368088589650558, -157.7092006025412 ] ],
  [ [ 21.36804367388635, -157.70915237129387 ] ],
  [ [ 21.368088589650558, -157.70929706503583 ] ],
  [ [ 21.36804367388635, -157.70915237129387 ] ],
  [ [ 21.367998758122148, -157.70910414004655 ] ],
  [ [ 21.367998758122148, -157.70939352753047 ] ]
] ,
[
  [ [ 21.36804367388635, -157.70934529646067 ] ],
  [ [ 21.367998758122145, -157.70929706524294 ] ],
  [ [ 21.367953842357938, -157.7092488340252 ] ],
  [ [ 21.367998758122145, -157.7093935276784 ] ],
  [ [ 21.367953842357938, -157.7092488340252 ] ],
  [ [ 21.367908926593735, -157.70920060280747 ] ],
  [ [ 21.367908926593735, -157.70948999011387 ] ]
] ,
[
  [ [ 21.36795384235794, -157.70944175913283 ] ],
  [ [ 21.367908926593735, -157.70939352794468 ] ],
  [ [ 21.36786401082953, -157.70934529675654 ] ],
  [ [ 21.367908926593735, -157.70948999032098 ] ],
  [ [ 21.36786401082953, -157.70934529675654 ] ],
  [ [ 21.367819095065325, -157.7092970655684 ] ],
  [ [ 21.367819095065325, -157.70958645269727 ] ]
] ,
[
  [ [ 21.36786401082953, -157.70953822180496 ] ],
  [ [ 21.36781909506532, -157.7094899906464 ] ],
  [ [ 21.367774179301115, -157.70944175948785 ] ],
  [ [ 21.36781909506532, -157.70958645296352 ] ],
  [ [ 21.367774179301115, -157.70944175948785 ] ],
  [ [ 21.367729263536912, -157.7093935283293 ] ],
  [ [ 21.367729263536912, -157.70968291528064 ] ]
] ,
[
  [ [ 21.36777417930112, -157.70963468447712 ] ],
  [ [ 21.367729263536912, -157.70958645334815 ] ],
  [ [ 21.367684347772705, -157.70953822221918 ] ],
  [ [ 21.367729263536912, -157.7096829156061 ] ],
  [ [ 21.367684347772705, -157.70953822221918 ] ],
  [ [ 21.367639432008502, -157.7094899910902 ] ],
  [ [ 21.367639432008502, -157.70977937786404 ] ]
] ,
[
  [ [ 21.367684347772705, -157.70973114714928 ] ],
  [ [ 21.3676394320085, -157.7096829160499 ] ],
  [ [ 21.367594516244292, -157.70963468495052 ] ],
  [ [ 21.3676394320085, -157.70977937824867 ] ],
  [ [ 21.367594516244292, -157.70963468495052 ] ],
  [ [ 21.36754960048009, -157.70958645385113 ] ],
  [ [ 21.36754960048009, -157.70987584044744 ] ]
] ,
[
  [ [ 21.367594516244292, -157.70982760982145 ] ],
  [ [ 21.367549600480086, -157.70977937875165 ] ],
  [ [ 21.36750468471588, -157.70973114768185 ] ],
  [ [ 21.367549600480086, -157.70987584089124 ] ],
  [ [ 21.36750468471588, -157.70973114768185 ] ],
  [ [ 21.367459768951676, -157.70968291661202 ] ],
  [ [ 21.367459768951676, -157.70997230303087 ] ]
] ,
[
  [ [ 21.367504684715882, -157.7099240724936 ] ],
  [ [ 21.367459768951676, -157.7098758414534 ] ],
  [ [ 21.36741485318747, -157.70982761041319 ] ],
  [ [ 21.367459768951676, -157.70997230353382 ] ],
  [ [ 21.36741485318747, -157.70982761041319 ] ],
  [ [ 21.367369937423266, -157.70977937937295 ] ],
  [ [ 21.367369937423266, -157.71006876561427 ] ]
] ,
[
  [ [ 21.36741485318747, -157.71002053516577 ] ],
  [ [ 21.367369937423263, -157.70997230415514 ] ],
  [ [ 21.367325021659056, -157.7099240731445 ] ],
  [ [ 21.367369937423263, -157.7100687661764 ] ],
  [ [ 21.367325021659056, -157.7099240731445 ] ],
  [ [ 21.367280105894853, -157.70987584213387 ] ],
  [ [ 21.367280105894853, -157.71016522819767 ] ]
] ,
[
  [ [ 21.367325021659056, -157.71011699783793 ] ],
  [ [ 21.36728010589485, -157.7100687668569 ] ],
  [ [ 21.367235190130643, -157.71002053587583 ] ],
  [ [ 21.36728010589485, -157.71016522881897 ] ],
  [ [ 21.367235190130643, -157.71002053587583 ] ],
  [ [ 21.36719027436644, -157.7099723048948 ] ],
  [ [ 21.36719027436644, -157.71026169078107 ] ]
] ,
[
  [ [ 21.367235190130646, -157.7102134605101 ] ],
  [ [ 21.36719027436644, -157.71016522955864 ] ],
  [ [ 21.367145358602233, -157.71011699860716 ] ],
  [ [ 21.36719027436644, -157.71026169146154 ] ],
  [ [ 21.367145358602233, -157.71011699860716 ] ],
  [ [ 21.36710044283803, -157.7100687676557 ] ],
  [ [ 21.36710044283803, -157.71035815336447 ] ]
] ,
[
  [ [ 21.367145358602233, -157.71030992318225 ] ],
  [ [ 21.367100442838026, -157.7102616922604 ] ],
  [ [ 21.36705552707382, -157.7102134613385 ] ],
  [ [ 21.367100442838026, -157.7103581541041 ] ],
  [ [ 21.36705552707382, -157.7102134613385 ] ],
  [ [ 21.367010611309617, -157.71016523041664 ] ],
  [ [ 21.367010611309617, -157.71045461594787 ] ]
] ,
[
  [ [ 21.36705552707382, -157.7104063858544 ] ],
  [ [ 21.367010611309613, -157.7103581549621 ] ],
  [ [ 21.366965695545407, -157.71030992406983 ] ],
  [ [ 21.367010611309613, -157.71045461674672 ] ],
  [ [ 21.366965695545407, -157.71030992406983 ] ],
  [ [ 21.366920779781204, -157.71026169317753 ] ],
  [ [ 21.366920779781204, -157.7105510785313 ] ]
] ,
[
  [ [ 21.36696569554541, -157.71050284852654 ] ],
  [ [ 21.366920779781204, -157.71045461766383 ] ],
  [ [ 21.366875864016997, -157.71040638680114 ] ],
  [ [ 21.366920779781204, -157.71055107938926 ] ],
  [ [ 21.366875864016997, -157.71040638680114 ] ],
  [ [ 21.366830948252794, -157.71035815593842 ] ],
  [ [ 21.366830948252794, -157.71064754111467 ] ]
] ,
[
  [ [ 21.366875864016997, -157.7105993111987 ] ],
  [ [ 21.36683094825279, -157.71055108036558 ] ],
  [ [ 21.366786032488584, -157.71050284953245 ] ],
  [ [ 21.36683094825279, -157.71064754203184 ] ],
  [ [ 21.366786032488584, -157.71050284953245 ] ],
  [ [ 21.36674111672438, -157.71045461869934 ] ],
  [ [ 21.36674111672438, -157.71074400369807 ] ]
] ,
[
  [ [ 21.366786032488587, -157.71069577387087 ] ],
  [ [ 21.36674111672438, -157.71064754306732 ] ],
  [ [ 21.366696200960174, -157.71059931226378 ] ],
  [ [ 21.36674111672438, -157.7107440046744 ] ],
  [ [ 21.366696200960174, -157.71059931226378 ] ],
  [ [ 21.36665128519597, -157.71055108146024 ] ],
  [ [ 21.36665128519597, -157.7108404662815 ] ]
] ,
[
  [ [ 21.366696200960174, -157.71079223654303 ] ],
  [ [ 21.366651285195967, -157.71074400576907 ] ],
  [ [ 21.36660636943176, -157.71069577499512 ] ],
  [ [ 21.366651285195967, -157.71084046731698 ] ],
  [ [ 21.36660636943176, -157.71069577499512 ] ],
  [ [ 21.366561453667558, -157.71064754422116 ] ],
  [ [ 21.366561453667558, -157.7109369288649 ] ]
] ,
[
  [ [ 21.36660636943176, -157.7108886992152 ] ],
  [ [ 21.366561453667554, -157.71084046847082 ] ],
  [ [ 21.366516537903347, -157.71079223772645 ] ],
  [ [ 21.366561453667554, -157.71093692995956 ] ],
  [ [ 21.366516537903347, -157.71079223772645 ] ],
  [ [ 21.366471622139144, -157.71074400698208 ] ],
  [ [ 21.366471622139144, -157.7110333914483 ] ]
] ,




april_ip = "10.202.0.1" 
casey_ip = "10.202.1.1"
donatello_ip = "10.202.2.1"
leonardo_ip = "10.202.3.1"
michelangelo_ip = "10.202.4.1"
raphael_ip = "10.202.5.1"
splinter_ip = "10.202.6.1"

april = olympe.Drone(april_ip)
casey = olympe.Drone(casey_ip)
donatello = olympe.Drone(donatello_ip)
leonardo = olympe.Drone(leonardo_ip)
michelangelo = olympe.Drone(michelangelo_ip)
raphael = olympe.Drone(raphael_ip)
splinter = olympe.Drone(splinter_ip)

# april.connection()
# casey.connection()

swarm = [casey, donatello, leonardo, michelangelo, raphael, splinter]
april.connection()
for drone in swarm:
    drone.connection()

# Take-off
def takeOff(drone):
    drone(
        FlyingStateChanged(state="hovering", _policy="check")
        | FlyingStateChanged(state="flying", _policy="check")
        | (
            GPSFixStateChanged(fixed=1, _timeout=10, _policy="check_wait")
            >> (
                TakeOff(_no_expect=True)
                & FlyingStateChanged(
                    state="hovering", _timeout=10, _policy="check_wait")
            )
        )
    ).wait()

takeOff(april)
for drone in swarm:
    takeOff(drone)



def moveSwarm(poi):
    casey(
        moveTo(poi[0][1][0],  poi[0][1][1], 0.9, MoveTo_Orientation_mode.TO_TARGET, 0.0)
        >> PCMD(1, 0, 0, 0, 0, 0)
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait().success()
    donatello(
        moveTo(poi[0][2][0],  poi[0][2][1], 0.8, MoveTo_Orientation_mode.TO_TARGET, 0.0)
        >> PCMD(1, 0, 0, 0, 0, 0)
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait().success()
    leonardo(
        moveTo(poi[0][3][0],  poi[0][3][1], 1.1, MoveTo_Orientation_mode.TO_TARGET, 0.0)
        >> PCMD(1, 0, 0, 0, 0, 0)
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait().success()
    michelangelo(
        moveTo(poi[0][4][0],  poi[0][4][1], 0.7, MoveTo_Orientation_mode.TO_TARGET, 0.0)
        >> PCMD(1, 0, 0, 0, 0, 0)
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait().success()
    raphael(
        moveTo(poi[0][5][0],  poi[0][5][1], 1.2, MoveTo_Orientation_mode.TO_TARGET, 0.0)
        >> PCMD(1, 0, 0, 0, 0, 0)
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait().success()
    splinter(
        moveTo(poi[0][6][0],  poi[0][6][1], 0.6, MoveTo_Orientation_mode.TO_TARGET, 0.0)
        >> PCMD(1, 0, 0, 0, 0, 0)
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait().success()







def move(coords):
    april(
        moveTo(coords[0][0][0], coords[0][0][1], 1, MoveTo_Orientation_mode.TO_TARGET, 0.0)
        >> PCMD(1, 0, 0, 0, 0, 0)
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait().success()
    moveSwarm(coords)




for coords in route:
    move(coords)



    





