# Inputs and output to/from XLA models are always in replicated mode. The shapes
# are [NUM_REPLICAS][NUM_VALUES]. A non replicated, single core, execution will
# has NUM_REPLICAS == 1, but retain the same shape rank.

# Colabにtorch_xlaモジュールをpullする
!pip install \
  http://storage.googleapis.com/pytorch-tpu-releases/tf-1.13/torch-1.0.0a0+1d94a2b-cp36-cp36m-linux_x86_64.whl  \
  http://storage.googleapis.com/pytorch-tpu-releases/tf-1.13/torch_xla-0.1+5622d42-cp36-cp36m-linux_x86_64.whl

import torch
import torch.nn as nn
import torch_xla

# TPUに載せるモデル
class XlaMulAdd(nn.Module):
  def forward(self, x, y):
    return x * y + y

# モデルへの入力
x = torch.rand(3, 5)
y = torch.rand(3, 5)

# モデルの宣言
model = XlaMulAdd()

# よくわからん
traced_model = torch.jit.trace(model, (x, y))
xla_model = torch_xla._XLAC.XlaModule(traced_model)
output_xla = xla_model((torch_xla._XLAC.XLATensor(x), torch_xla._XLAC.XLATensor(y)))
expected = model(x, y)
print(output_xla[0][0].to_tensor().data)
print(expected.data)
