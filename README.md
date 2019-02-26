# RoboPython
未完
## 概要
robocupサッカーシミュレーション2Dリーグで使用できる選手エージェントのプログラム。
参考文献１のサンプルのjavaで書かれたエージェントプログラムをpythonで書き換えたもの。
フォルダsrc内にエージェントプログラムは格納されている

## プログラムの説明
以下のプログラムは若い数字から順々にプログラムを継承させていったものである。
すなわち自身より若い数字のエージェントの機能をエージェントはすでに備えているように設計してある。

### player0.py
ソケット通信によってエージェントを１名だけ試合に登録するプログラム

### player1.py
ソケット通信・threadingによってエージェントを複数人数、試合に登録するプログラム

### player2.py
試合に登録したエージェントを試合前に指定位置に瞬間移動させるプログラム

### player3.py
試合開始後「kick_off」モード時はエージェント全員が時計回りに、「play_on」モード時は反時計回りに回転させるプログラム

### player4.py
試合開始後、すべてのエージェントをボールの方向に向かせるプログラム

### player5.py
試合開始後、エージェント全員がボールに向かって走り、ボールを蹴ることのできる状況になったら相手ゴール方向、もしくは自身の斜め後ろ方向にボールを
蹴らせるプログラム（いわゆる幼稚園サッカープログラム）

### player6.py
ボールに一番近いエージェントのみがボールを追いかけさせる。
また、前に出すぎたエージェントを自陣に戻すことも行う。
試合はplayer6のエージェントチームとplayer5のエージェントチームの対戦で行われる

### player7.py
ボールを見ずとも向いている方向を計算しゴール方向にシュートを行わせるプログラム。
（今まではゴールの見えないときは自身の斜め後ろ方向または体ごと向きを直してシュートを行わせていた）
試合はplayer7のエージェントチームとplayer6のエージェントチームの対戦で行われる

### player8.py
エージェント自身の位置を視覚情報を利用して認識させるプログラム
試合時の能力的な変化はplayer7と比べてはない

### player9.py
ボールの位置を視覚情報を利用して認識させる
その情報から自身の適切な守備位置を計算させる
試合時の能力的な変化はplayer8と比べてはない

### player10.py
計算した守備位置またはボール方向に逐次移動するプログラム。
（いわゆるゾーンディフェンスを行う）
試合はplayer10のエージェントチームとplayer9のエージェントチームの対戦で行われる

### player11.py
過去のフィールドの状況から現在のフィールドの状況を予測し、それに基づいたコマンドをサーバーに送信する準備を行うプログラム
（今までは過去の視覚情報からコマンドを決定していたのでそのタイムラグによってエージェントが誤動作してしまうことがあった）

### player12.py
move（瞬間移動）コマンドを利用したときにエージェントの位置を予測させるプログラム

### player13.py
dash（移動）コマンドを利用したときにエージェントの位置を予測させるプログラム（スタミナについての考慮はしていない）

### player14.py
スタミナ係数の読み込みのみを行うプログラム

### player15.py
スタミナモデルを考慮したdash（移動）コマンドを利用したときにエージェントの位置を予測を行わせるプログラム

（以下のエージェントはまだ理想とする挙動を実現できていない）
### player16.py
体、首の方向（turn, turn_neckコマンド利用時の結果）を予測させるプログラム

### player17.py
ボールの位置（kickコマンド利用時の結果）を予測させるプログラム

### player18.py
視界に入っているボールの情報を計算させるプログラム


以下のエージェントは明らかに目的の挙動を実現できていない状況である

### player19.py
ボールを視界に捉え続けようとするプログラム

### player20.py


### player21.py
背番号10が常にボールを追いかけるプログラム

### player22.py
一番近い選手のみがボールに移動。
他の選手は守備位置に移動

### player23.py
ボールのトラップする位置を予測する。


### player24.py
トラップ位置で正確なキックを実行するプログラム

### player25.py
パス地点を評価してキックするプログラム


## 参考文献
1. 大島真樹「javaでつくるRoboCupサッカー選手プログラム」(2005) 森北出版株式会社
http://www.morikita.co.jp/books/book/2189
2. https://ameblo.jp/oyasai10/entry-10590541669.html
3. http://edosha.hatenablog.jp/entry/2017/08/09/150636
4. https://www.kannon.link/fuku/index.php/2017/02/22/01-34/
