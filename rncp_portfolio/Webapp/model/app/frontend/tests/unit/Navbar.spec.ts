import { render, screen } from '@testing-library/vue'
import Navbar from '@/components/Navbar.vue'

test('affiche les liens principaux', () => {
    render(Navbar)
    expect(screen.getByText('Mon compte')).toBeTruthy()
})
