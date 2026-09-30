from guilde_data.generator import generate_company


def test_generate_company_is_deterministic():
    a = generate_company(42)
    b = generate_company(42)
    assert a.to_dict() == b.to_dict()


def test_generate_company_has_expected_shape():
    c = generate_company(7)
    assert c.company_name
    assert len(c.npcs) == 3
    assert any(p.kind == "client" for p in c.parties)
    assert any(p.kind == "supplier" for p in c.parties)
    assert len(c.invoices) >= 1
    assert len(c.exchanges) >= 1
    assert c.seed == 7


def test_different_seeds_differ():
    assert generate_company(1).to_dict() != generate_company(2).to_dict()
