## 10.3 ユニットテスト

- `TestBed`のメソッド
	- `configuretestingModule(def)`：テスト対象のコンポーネントを本来のアプリモジュールから切り離す。
	- `createComponent(comp)`：コンポーネントをインスタンス化する

>**分離単体テスト**
>コンポーネントは，Angularに強く依存しているため，テスト専用のTest APIが用意されているが，パイプ・サービスのテストは標準的なJasmineのAPIで行うことができる。後者を，分離単体テストという。後者の場合，ソースコードがシンプルで見やすくなるため，こっちの方が推奨される。

- コンポーネントの中に外部テンプレートが含まれる場合，読み込んだときに`.compileComponents()`でコンパイルする必要がある。

>**テスト駆動開発**
>- 最初にテストを書き，とりあえずの実装を行い，より洗練させていくという開発スタイル。
>-  "Clean code that works" が目標。そのために，まずテストに通るコードを作成し，それをリファクタリングする方法をとる。

>**ビヘイビア駆動開発**
>- コードレベル，ユーザレベルで，期待される振る舞いをテストコードに記述する。
>- 自然言語に近い形で，振る舞いを記述できるフレームワークが多いらしい。

---

### コンポーネントのテスト
**コンポーネント**のテストコード例：
```js
import { AppComponent } from './app.component';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ComponentFixtureAutoDetect } from '@angular/core/testing';

import { By }           from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

// テストスクリプト本体（は，describe()で囲まれる）
describe('AppComponent', function () {
  let de: DebugElement;
  let comp: AppComponent;
  let fixture: ComponentFixture<AppComponent>;

  beforeEach(() => {
    // テストモジュールを準備
    TestBed.configureTestingModule({
      declarations: [ AppComponent ],
      // ComponentFixtureAutoDetect を用いると，detectChanges()しなくても変更検知してくれるようになる。
      providers: [
        { provide: ComponentFixtureAutoDetect, useValue: true }
      ]
    });
    
    // コンポーネントをインスタンス化
    fixture = TestBed.createComponent(AppComponent);
    comp = fixture.componentInstance;
    //テスト対象の要素を取得
    de = fixture.debugElement.query(By.css('h1'));
  });
  
  // <h1>要素の配下に「angular」の文字列が含まれているかを検証
  it('<h1>要素のテキストを確認', () => {
    fixture.detectChanges();
    const h1 = de.nativeElement;
    expect(h1.innerText).toMatch(/angular/i);
  });
  
  // nameプロパティの更新がテンプレートに反映されているかを検証
  it('nameプロパティの変化を確認', () => {
    comp.name = 'JavaScript';
    fixture.detectChanges();
    const h1 = de.nativeElement;
    expect(h1.innerText).toMatch(/javascript/i);
  });
});
```

- `TestBed`：ユニットテストのための環境を初期化・設定するためのクラス
- `createComponent(comp)`：コンポーネントのインスタンス化を行う。返ってくるオブジェクトは，`ComponentFixture`オブジェクトである。

---

### 外部テンプレートを含むコンポーネントのテスト
- コンポーネントに外部テンプレートが含まれる場合，テストも若干複雑になる。
- `beforeEach(async({外部テンプレートのコンパイル}))` みたいな形で，非同期的に外部テンプレートのコンパイルを行う必要があるらしい。そうすると，ここでの処理が終わった後に後続の処理が呼ばれる（なぜそうする？）

例：
```js
import { DebugElement } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By }           from '@angular/platform-browser';

import { AppComponent } from './app.component';

describe('AppComponent', function () {
  let des: DebugElement[];
  let comp: AppComponent;
  let fixture: ComponentFixture<AppComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AppComponent ],
    })
    .compileComponents();
  }));

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AppComponent ],
    })
    .compileComponents()
    .then((result) => {
      fixture = TestBed.createComponent(AppComponent);
      comp = fixture.componentInstance;
      des = fixture.debugElement.queryAll(By.css('tr'));
    });
  }));

    beforeEach(() => {
      fixture = TestBed.createComponent(AppComponent);
      comp = fixture.componentInstance;
    });

  it('テーブルの行数を確認', () => {
    fixture.detectChanges();
    des = fixture.debugElement.queryAll(By.css('tr'));
    expect(des.length).toEqual(6);
  });
});
```

- 最初の`beforeEach()`でコンパイルを，後続の`beforeEach()`でインスタンス化を行う。
- ここに特記すべきことではないが，`beforeEach()`は，後続の複数のテストに共通する前処理を行うためのものである。
