import torch
from torch_geometric.nn import global_sort_pool


def test_global_sort_pool():
    N_1, N_2 = 4, 6
    x = torch.randn(N_1 + N_2, 4)
    batch = torch.tensor([0 for _ in range(N_1)] + [1 for _ in range(N_2)])

    out = global_sort_pool(x, batch, k=5)
    assert out.size() == (2, 5 * 4)
    out = out.view(2, 5, 4)

    # Features are individually sorted.
    expected = torch.arange(4).view(1, 1, 4).expand_as(out)
    assert out.argsort(dim=2).tolist() == expected.tolist()

    # First graph output has been filled up with zeros.
    assert out[0, -1].tolist() == [0, 0, 0, 0]

    # Nodes are sorted.
    expected = 4 - torch.arange(5).view(1, 5).expand(2, 5)
    assert out.argsort(dim=1)[:, :, -1].tolist() == expected.tolist()
